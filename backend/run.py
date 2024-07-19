from app import create_app
import os
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('BACKEND_PORT', 5001))
    debug_mode = os.getenv('DEBUG', 'True') == 'True'
    print("BACKEND_PORT =", port)    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)