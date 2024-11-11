# Mautic Website Analyzer

A Python tool for analyzing WordPress websites through Mautic contacts.

## Overview
This tool integrates with Mautic API to analyze WordPress websites associated with contacts and update their information.

## Development Setup
- Python 3.8+ required
- Virtual environment (./venv)
- Configuration via .env file
- Local development with cloud deployment capability

## Project Structure
- `/src`: Main source code and modules
- `/backups`: Development backups (see backups/README.md)
- `/tools`: Utility scripts and tools
- `/config`: Configuration files
- `/venv`: Virtual environment (not tracked)

## Documentation
- `PROJECT.md`: Detailed project structure and workflow
- `backups/README.md`: Backup conventions and methodology
- `.env.example`: Environment variable template

## Getting Started
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure
6. Run: `./run_analyzer.sh`
