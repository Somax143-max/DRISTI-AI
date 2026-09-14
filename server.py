import os
import sys
import json
import base64
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import cv2
import numpy as np

# Import our trained PyTorch and OpenCV retinal analyzer
import retina_analyzer
from app.validators.input_sanitizer import validate_and_sanitize_image
from app.monitoring.drift_detector import get_drift_monitor

class DrishtiAIHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path in ['/api/health', '/api/status']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'HEALTHY',
                'service': 'DRISHTI AI Inference Engine',
                'version': '2.0.0-SIH26038'
            }).encode('utf-8'))
            return
        elif self.path == '/api/drift-status':
            drift_report = get_drift_monitor().audit_drift()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(drift_report).encode('utf-8'))
            return
        super().do_GET()

    def do_POST(self):
        if self.path in ['/api/analyze', '/api/analyze-retina']:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                image_b64 = data.get('image', '')
                if not image_b64:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'No image data provided in payload'}).encode('utf-8'))
                    return

                # Validate and decode via Input Sanitizer (Item 50)
                is_valid, img_bgr, meta, err = validate_and_sanitize_image(image_b64)
                if not is_valid:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': err or 'Image validation failed'}).encode('utf-8'))
                    return

                # Execute real PyTorch and OpenCV retinal analysis
                result = retina_analyzer.analyze_retinal_fundus(img_bgr)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8080):
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, DrishtiAIHandler)
    print(f"DRISHTI AI Real Retinal Verification & Diagnostic Server running on port {port}...")
    sys.stdout.flush()
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
