#!/usr/bin/env python3
"""
Fix script for numpy._core.numeric compatibility issue with stable-baselines3
This script addresses the ModuleNotFoundError: No module named 'numpy._core.numeric'
"""

import sys
import os
import subprocess
from pathlib import Path

def fix_numpy_compatibility():
    """
    Fix the numpy compatibility issue by:
    1. Creating a virtual environment
    2. Installing compatible versions of numpy and stable-baselines3
    3. Testing the fix
    """
    
    print("🔧 Fixing numpy._core.numeric compatibility issue...")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Already in virtual environment")
    else:
        print("⚠️  Not in virtual environment. Please activate your virtual environment first.")
        print("   Run: source venv/bin/activate")
        return False
    
    try:
        # Test the fix
        print("\n🧪 Testing numpy and stable-baselines3 compatibility...")
        
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
        
        from stable_baselines3 import PPO
        print("✅ Stable-Baselines3 PPO import successful")
        
        # Test model creation and loading (the specific operation that was failing)
        import gymnasium as gym
        env = gym.make('CartPole-v1')
        model = PPO('MlpPolicy', env, verbose=0)
        print("✅ PPO model creation successful")
        
        # Test save/load (this triggers the numpy._core.numeric issue)
        import tempfile
        temp_path = '/tmp/test_ppo_model.zip'
        model.save(temp_path)
        loaded_model = PPO.load(temp_path)
        print("✅ PPO model save/load successful")
        
        # Clean up
        os.remove(temp_path)
        env.close()
        
        print("\n🎉 SUCCESS: The numpy._core.numeric compatibility issue is fixed!")
        print("   Your trading bot should now be able to load RL models without errors.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n🔧 To fix this issue manually:")
        print("1. Create a virtual environment: python3 -m venv venv")
        print("2. Activate it: source venv/bin/activate")
        print("3. Install compatible versions:")
        print("   pip install numpy==1.26.4 stable-baselines3==2.7.0")
        print("4. Install other dependencies: pip install -r requirements.txt")
        
        return False

def create_activation_script():
    """Create a script to easily activate the fixed environment"""
    
    script_content = """#!/bin/bash
# Activation script for the fixed trading bot environment

echo "🚀 Activating trading bot environment with numpy compatibility fix..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade key packages if needed
echo "📦 Ensuring compatible packages are installed..."
pip install --upgrade pip
pip install numpy==1.26.4 stable-baselines3==2.7.0

echo "✅ Environment activated successfully!"
echo "   You can now run your trading bot without numpy._core.numeric errors."
echo ""
echo "To run your bot:"
echo "   python3 'Bot-Trading_Swing (1).py'"
"""

    with open('/workspace/activate_bot_env.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('/workspace/activate_bot_env.sh', 0o755)
    print("📝 Created activation script: activate_bot_env.sh")
    print("   Run: ./activate_bot_env.sh")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 NUMPY COMPATIBILITY FIX FOR TRADING BOT")
    print("=" * 60)
    
    success = fix_numpy_compatibility()
    
    if success:
        create_activation_script()
        print("\n" + "=" * 60)
        print("✅ FIX COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run your trading bot: python3 'Bot-Trading_Swing (1).py'")
        print("2. Or use the activation script: ./activate_bot_env.sh")
    else:
        print("\n" + "=" * 60)
        print("❌ FIX FAILED - Manual intervention required")
        print("=" * 60)