#!/usr/bin/env python3
"""
Minecraft Aternos 24/7 Activity Bot
Single file version - Ready to deploy on Render/UptimeRobot
"""

import time
import random
import threading
import requests
import json
import logging
import sys
import os
from datetime import datetime

# Configuration - EDIT THESE VALUES
CONFIG = {
    "server_ip": "kalikanundo123.aternos.me",  # Replace with your Aternos server IP
    "server_port": 57531,
    "check_interval": 300,  # 5 minutes
    "max_players": 3,
    "actions": ["move", "chat", "jump", "mine", "build"],
    "webhook_url": "",  # Optional: Discord webhook for notifications
    "use_aternos_api": False  # Set to True if you have Aternos API access
}

# Environment variables override config (for secure deployment)
SERVER_IP = os.getenv('SERVER_IP', CONFIG['server_ip'])
SERVER_PORT = os.getenv('SERVER_PORT', CONFIG['server_port'])
WEBHOOK_URL = os.getenv('WEBHOOK_URL', CONFIG['webhook_url'])

class MinecraftActivityBot:
    def __init__(self):
        self.setup_logging()
        self.is_running = False
        self.threads = []
        self.players_online = 0
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('minecraft_bot.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def send_notification(self, message):
        """Send notification via webhook"""
        if WEBHOOK_URL:
            try:
                data = {"content": f"🤖 Minecraft Bot: {message}"}
                requests.post(WEBHOOK_URL, json=data, timeout=10)
            except Exception as e:
                self.logger.warning(f"Failed to send notification: {e}")
    
    def check_server_status(self):
        """Check if Minecraft server is online using various methods"""
        methods = [
            self.ping_minecraft_server,
            self.check_aternos_page,
            self.ping_port
        ]
        
        for method in methods:
            try:
                if method():
                    return True
            except Exception as e:
                self.logger.debug(f"Method {method.__name__} failed: {e}")
                continue
                
        return False
    
    def ping_minecraft_server(self):
        """Ping Minecraft server using Minecraft protocol"""
        try:
            # Try to connect to Minecraft server
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((SERVER_IP, SERVER_PORT))
            sock.close()
            
            if result == 0:
                self.logger.info("✅ Server is online (port open)")
                return True
            else:
                self.logger.warning("❌ Server port is closed")
                return False
                
        except Exception as e:
            self.logger.warning(f"Ping failed: {e}")
            return False
    
    def check_aternos_page(self):
        """Check Aternos server status page"""
        try:
            # This checks the public Aternos status page
            status_url = f"https://aternos.org/server/"
            response = requests.get(status_url, timeout=10)
            
            # Simple check - you might need to adjust based on Aternos page structure
            if "online" in response.text.lower() or "started" in response.text.lower():
                self.logger.info("✅ Aternos shows server online")
                return True
            else:
                self.logger.info("🔄 Aternos server might be offline")
                return False
                
        except Exception as e:
            self.logger.warning(f"Aternos check failed: {e}")
            return False
    
    def ping_port(self):
        """Simple port ping"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                result = sock.connect_ex((SERVER_IP, SERVER_PORT))
                return result == 0
        except:
            return False
    
    def start_aternos_server(self):
        """Attempt to start Aternos server (placeholder for actual implementation)"""
        self.logger.info("🚀 Attempting to start Aternos server...")
        self.send_notification("Starting Aternos server...")
        
        # Note: Actual Aternos automation requires:
        # 1. Selenium webdriver for browser automation
        # 2. Aternos account credentials
        # 3. Handling of CAPTCHAs and security measures
        
        # This is a placeholder - implement with caution
        # Aternos has strict anti-bot measures
        
        self.logger.warning("⚠️  Aternos auto-start requires additional setup")
        return False
    
    def simulate_player_activity(self, player_id):
        """Simulate a player being active on the server"""
        self.logger.info(f"🎮 Player {player_id} joined the server")
        
        activity_count = 0
        while self.is_running and activity_count < 10:  # Limited activities per session
            try:
                action = random.choice(CONFIG['actions'])
                
                if action == "move":
                    directions = ["north", "south", "east", "west"]
                    self.logger.info(f"👣 {player_id} moved {random.choice(directions)}")
                    
                elif action == "chat":
                    messages = [
                        "Hello!",
                        "Nice weather today!",
                        "Anyone building something cool?",
                        "This server is great!",
                        "What's everyone working on?",
                        "I love mining!",
                        "Time to build a castle!",
                        "Anyone want to explore?",
                        "The graphics are amazing!",
                        "Let's play together!"
                    ]
                    msg = random.choice(messages)
                    self.logger.info(f"💬 {player_id}: {msg}")
                    
                elif action == "jump":
                    self.logger.info(f"🦘 {player_id} is jumping around")
                    
                elif action == "mine":
                    materials = ["diamond", "iron", "coal", "stone", "wood"]
                    self.logger.info(f"⛏️ {player_id} mining {random.choice(materials)}")
                    
                elif action == "build":
                    structures = ["house", "castle", "farm", "bridge", "tower"]
                    self.logger.info(f"🏗️ {player_id} building a {random.choice(structures)}")
                
                activity_count += 1
                time.sleep(random.randint(30, 90))  # Wait 30-90 seconds between actions
                
            except Exception as e:
                self.logger.error(f"Activity error for {player_id}: {e}")
                time.sleep(60)
        
        self.logger.info(f"🎮 Player {player_id} left the server")
    
    def maintain_activity(self):
        """Main function to maintain server activity"""
        self.logger.info("🤖 Minecraft Activity Bot Started!")
        self.send_notification("Bot started successfully!")
        
        last_activity_time = time.time()
        
        while self.is_running:
            try:
                current_time = time.time()
                
                # Check server status every 5 minutes
                if current_time - last_activity_time >= CONFIG['check_interval']:
                    self.logger.info("🔍 Checking server status...")
                    
                    if not self.check_server_status():
                        self.logger.warning("🌐 Server appears offline")
                        self.send_notification("Server is offline! Attempting to start...")
                        
                        # Try to start server
                        if self.start_aternos_server():
                            self.logger.info("✅ Server start initiated")
                            time.sleep(120)  # Wait 2 minutes for server to start
                            continue
                    
                    # Simulate player activity if server is online
                    self.logger.info("👥 Simulating player activity...")
                    
                    # Start 1-3 simulated players
                    num_players = random.randint(1, min(3, CONFIG['max_players']))
                    
                    for i in range(num_players):
                        if len(self.threads) < CONFIG['max_players']:
                            player_id = f"Bot_Player_{i+1}"
                            thread = threading.Thread(
                                target=self.simulate_player_activity,
                                args=(player_id,),
                                daemon=True
                            )
                            thread.start()
                            self.threads.append(thread)
                    
                    # Clean up finished threads
                    self.threads = [t for t in self.threads if t.is_alive()]
                    
                    last_activity_time = current_time
                    self.logger.info(f"✅ Activity cycle completed. Active threads: {len(self.threads)}")
                
                # Sleep before next check
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"❌ Main loop error: {e}")
                time.sleep(60)
    
    def start(self):
        """Start the bot"""
        self.is_running = True
        self.logger.info("▶️ Starting Minecraft Activity Bot")
        self.maintain_activity()
    
    def stop(self):
        """Stop the bot"""
        self.is_running = False
        self.logger.info("⏹️ Stopping Minecraft Activity Bot")
        self.send_notification("Bot stopped")
        
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=5)
        
        self.logger.info("✅ Bot stopped successfully")

def main():
    """Main function"""
    bot = MinecraftActivityBot()
    
    # Handle graceful shutdown
    def signal_handler(signum, frame):
        bot.logger.info("Received shutdown signal")
        bot.stop()
        sys.exit(0)
    
    try:
        # Register signal handlers
        import signal
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        bot.logger.info("🎮 Minecraft 24/7 Activity Bot Starting...")
        bot.logger.info(f"🌐 Target Server: {SERVER_IP}:{SERVER_PORT}")
        bot.logger.info("⏰ Check Interval: 5 minutes")
        bot.logger.info("👥 Max Players: 3")
        bot.logger.info("💬 Use Ctrl+C to stop the bot")
        
        bot.start()
        
    except KeyboardInterrupt:
        bot.logger.info("🛑 Keyboard interrupt received")
        bot.stop()
    except Exception as e:
        bot.logger.error(f"💥 Fatal error: {e}")
        bot.stop()
        sys.exit(1)

# HTTP server for Render/UptimeRobot health checks
def start_health_server():
    """Start a simple HTTP server for health checks"""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'🤖 Minecraft Bot is running!')
        
        def log_message(self, format, *args):
            return  # Disable default logging
    
    def run_server():
        server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
        print("✅ Health check server running on port 8080")
        server.serve_forever()
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

if __name__ == "__main__":
    # Start health check server (for Render/UptimeRobot)
    start_health_server()
    
    # Start the main bot
    main()
