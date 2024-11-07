#!/usr/bin/env python3

import json
import os
from datetime import datetime

class CheckpointManager:
    def __init__(self, filename="checkpoint.json"):
        self.filename = filename
        self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'last_contact_id': None,
                'last_run': None,
                'total_processed': 0,
                'batch_stats': []
            }
    
    def save(self, contact_id, batch_time=None):
        self.data['last_contact_id'] = contact_id
        self.data['last_run'] = datetime.now().isoformat()
        self.data['total_processed'] += 1
        
        if batch_time:
            self.data['batch_stats'].append({
                'timestamp': datetime.now().isoformat(),
                'processing_time': batch_time
            })
            # Keep only last 100 batch stats
            self.data['batch_stats'] = self.data['batch_stats'][-100:]
        
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_last_contact_id(self):
        return self.data['last_contact_id']
    
    def get_stats(self):
        return {
            'total_processed': self.data['total_processed'],
            'last_run': self.data['last_run'],
            'avg_batch_time': sum(b['processing_time'] for b in self.data['batch_stats'][-10:]) / 10 if self.data['batch_stats'] else 0
        }
