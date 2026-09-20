#!/bin/bash

# ============================================
# env_install.sh - Development Environment Setup Script
# Purpose: Automates installation of essential dev tools
# ============================================

# --- Script Best Practices ---
# Strict mode: Exit on errors, treat unset vars as errors, fail pipelines
set -euo pipefail

# Quote variables to prevent word splitting bugs
# Use meaningful comments to explain WHY, not just WHAT

# --- Feature 1: Pretty Printing Function ---
pretty_print() {
    local message="$1"
    local color="$2"  # 1=green, 2=yellow, 3=red
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo -e "\n[$timestamp] $message"
}

# --- Feature 2: Operating System Detection ---
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux"
    else
        echo "Unknown ($OSTYPE)"
    fi
}

# --- Feature 3: Python Install Check ---
check_python() {
    pretty_print "Checking Python installation..." "1"
    
    if command -v python3 &> /dev/null; then
        local version
        version=$(python3 --version)
        pretty_print "✓ Python $version is installed" "1"
        return 0
    else
        pretty_print "✗ Python 3 is NOT installed" "3"
        return 1
    fi
}

# --- Feature 4: Pip Version Verification ---
check_pip() {
    pretty_print "Checking pip installation..." "1"
    
    if command -v pip3 &> /dev/null; then
        local version
        version=$(pip3 --version)
        pretty_print "✓ Pip $version is installed" "1"
        return 0
    else
        pretty_print "✗ Pip is NOT installed" "3"
        return 1
    fi
}

# --- Feature 5: Jupyter Notebook Installation ---
install_jupyter() {
    pretty_print "Installing Jupyter Notebook..." "2"
    local os_type
    os_type=$(detect_os)
    
    case "$os_type" in
        "Linux")
            if command -v pip3 &> /dev/null; then
                pip3 install jupyter --break-system-packages
                pretty_print "✓ Jupyter Notebook installed successfully" "1"
            else
                pretty_print "✗ Cannot install Jupyter: pip3 not found" "3"
                return 1
            fi
            ;;
        "macOS")
            if command -v pip3 &> /dev/null; then
                pip3 install jupyter --break-system-packages
                pretty_print "✓ Jupyter Notebook installed successfully" "1"
            else
                pretty_print "✗ Cannot install Jupyter: pip3 not found" "3"
                return 1
            fi
            ;;
        *)
            pretty_print "⚠ Jupyter installation skipped: Unknown OS" "2"
            ;;
    esac
}

# --- Main Execution Flow ---
main() {
    pretty_print "Starting Development Environment Setup..." "1"
    
    local os_type
    os_type=$(detect_os)
    pretty_print "Detected OS: $os_type" "1"
    
    # Check Python
    if ! check_python; then
        pretty_print "⚠ Python check failed. Please install Python 3 first." "2"
    fi
    
    # Check Pip
    if ! check_pip; then
        pretty_print "⚠ Pip check failed. Please install pip first." "2"
    fi
    
    # Install Jupyter
    install_jupyter
    
    
    pretty_print "Setup complete!" "1"
}

# Run main function
main
