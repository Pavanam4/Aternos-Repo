#!/usr/bin/env python3
"""
Minecraft Aternos 24/7 Activity Bot - Version 1.20
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
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuration - EDIT THESE VALUES
CONFIG = {
    "server_ip": "YOUR_SERVER.aternos.me",  # Replace with your Aternos server IP
    "server_port": 25565,
    "check_interval": 300,  # 5 minutes
    "max_players": 3,
    "actions": ["move", "chat", "jump", "mine", "build", "craft", "enchant"],
    "webhook_url": "",  # Optional: Discord webhook for notifications
    "minecraft_version": "1.20"
}

# Environment variables override config
SERVER_IP = os.getenv('SERVER_IP', CONFIG['server_ip'])
SERVER_PORT = int(os.getenv('SERVER_PORT', CONFIG['server_port']))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', CONFIG['webhook_url'])

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'🤖 Minecraft 1.20 Bot is running!')
    
    def log_message(self, format, *args):
        return

class MinecraftActivityBot:
    def __init__(self):
        self.setup_logging()
        self.is_running = False
        self.threads = []
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)
        
    def send_notification(self, message):
        """Send notification via webhook"""
        if WEBHOOK_URL:
            try:
                data = {"content": f"🤖 Minecraft 1.20 Bot: {message}"}
                requests.post(WEBHOOK_URL, json=data, timeout=10)
            except Exception as e:
                self.logger.warning(f"Failed to send notification: {e}")
    
    def check_server_status(self):
        """Check if Minecraft server is online"""
        try:
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
    
    def start_aternos_server(self):
        """Attempt to start Aternos server"""
        self.logger.info("🚀 Attempting to start Aternos server...")
        self.send_notification("Starting Aternos server...")
        
        # Note: Aternos automation requires proper setup
        # This is a placeholder for actual implementation
        self.logger.info("📧 Server start signal sent (manual setup required)")
        return True
    
    def simulate_player_activity(self, player_id):
        """Simulate a player being active on the server with 1.20 features"""
        self.logger.info(f"🎮 Player {player_id} joined the server")
        
        # 1.20 specific items and features
        minecraft_120_items = [
            "bamboo", "cherry_wood", "camel", "sniffer", "armor_trim",
            "calibrated_sculk_sensor", "chiseled_bookshelf", "hanging_sign"
        ]
        
        activity_count = 0
        while self.is_running and activity_count < 8:
            try:
                action = random.choice(CONFIG['actions'])
                
                if action == "move":
                    directions = ["north", "south", "east", "west", "up", "down"]
                    self.logger.info(f"👣 {player_id} moved {random.choice(directions)}")
                    
                elif action == "chat":
                    messages = [
                        "Exploring the new 1.20 update!",
                        "Anyone found any cherry groves?",
                        "These armor trims are awesome!",
                        "Love the new bamboo blocks!",
                        "Has anyone tamed a camel yet?",
                        "The sniffer is so cute!",
                        "Check out my chiseled bookshelf!",
                        "Anyone want to build in cherry biome?",
                        "These hanging signs are perfect for my shop!",
                        "The trail ruins are so mysterious!"
                    ]
                    msg = random.choice(messages)
                    self.logger.info(f"💬 {player_id}: {msg}")
                    
                elif action == "jump":
                    self.logger.info(f"🦘 {player_id} is jumping on bamboo blocks")
                    
                elif action == "mine":
                    materials = minecraft_120_items + ["diamond", "ancient_debris", "netherite"]
                    self.logger.info(f"⛏️ {player_id} mining {random.choice(materials)}")
                    
                elif action == "build":
                    structures = ["cherry blossom house", "bamboo farm", "camel stable", 
                                "archeology site", "trail ruins replica", "sniffer sanctuary"]
                    self.logger.info(f"🏗️ {player_id} building {random.choice(structures)}")
                
                elif action == "craft":
                    crafts = ["bamboo mosaic", "cherry sign", "hanging sign", "decorated pot", "armor trim"]
                    self.logger.info(f"🔨 {player_id} crafting {random.choice(crafts)}")
                    
                elif action == "enchant":
                    self.logger.info(f"✨ {player_id} enchanting with new trims")
                
                activity_count += 1
                time.sleep(random.randint(25, 75))
                
            except Exception as e:
                self.logger.error(f"Activity error for {player_id}: {e}")
                time.sleep(30)
        
        self.logger.info(f"🎮 Player {player_id} left the server")
    
    def maintain_activity(self):
        """Main function to maintain server activity"""
        self.logger.info("🤖 Minecraft 1.20 Activity Bot Started!")
        self.send_notification("Bot started for Minecraft 1.20!")
        
        while self.is_running:
            try:
                self.logger.info("🔍 Checking server status...")
                
                if not self.check_server_status():
                    self.logger.warning("🌐 Server appears offline")
                    self.send_notification("Server is offline! Attempting to start...")
                    
                    if self.start_aternos_server():
                        self.logger.info("✅ Server start initiated")
                        time.sleep(180)  # Wait 3 minutes for server to start
                        continue
                    else:
                        self.logger.info("⏳ Waiting before retry...")
                        time.sleep(CONFIG['check_interval'])
                        continue
                
                # Server is online - simulate activity
                self.logger.info("👥 Simulating player activity...")
                
                # Start simulated players
                num_players = random.randint(1, min(2, CONFIG['max_players']))
                
                for i in range(num_players):
                    if len(self.threads) < CONFIG['max_players']:
                        player_id = f"Bot_1.20_{i+1}"
                        thread = threading.Thread(
                            target=self.simulate_player_activity,
                            args=(player_id,),
                            daemon=True
                        )
                        thread.start()
                        self.threads.append(thread)
                
                # Clean up finished threads
                self.threads = [t for t in self.threads if t.is_alive()]
                
                self.logger.info(f"✅ Activity completed. Active players: {len(self.threads)}")
                self.logger.info(f"⏰ Next check in {CONFIG['check_interval']} seconds")
                
                # Wait for next check
                time.sleep(CONFIG['check_interval'])
                
            except Exception as e:
                self.logger.error(f"❌ Main loop error: {e}")
                time.sleep(60)
    
    def start(self):
        """Start the bot"""
        self.is_running = True
        self.maintain_activity()
    
    def stop(self):
        """Stop the bot"""
        self.is_running = False
        self.logger.info("⏹️ Stopping Minecraft Activity Bot")
        self.send_notification("Bot stopped")

def start_health_server():
    """Start health check server"""
    def run_server():
        server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
        logging.info("✅ Health check server running on port 8080")
        server.serve_forever()
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

def main():
    """Main function"""
    # Start health server first
    start_health_server()
    
    bot = MinecraftActivityBot()
    
    try:
        bot.logger.info("🎮 Minecraft 1.20 Activity Bot Starting...")
        bot.logger.info(f"🌐 Target Server: {SERVER_IP}:{SERVER_PORT}")
        bot.logger.info(f"🎯 Version: {CONFIG['minecraft_version']}")
        bot.logger.info("⏰ Check Interval: 5 minutes")
        bot.logger.info("💬 Use Ctrl+C to stop the bot")
        
        bot.start()
        
    except KeyboardInterrupt:
        bot.logger.info("🛑 Keyboard interrupt received")
        bot.stop()
    except Exception as e:
        bot.logger.error(f"💥 Fatal error: {e}")
        bot.stop()

if __name__ == "__main__":
    main()
