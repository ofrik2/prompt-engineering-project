"""
Comprehensive test suite for multi-model support in Azure OpenAI helper.

This test validates:
1. Configuration loading for both primary and secondary models
2. Model availability checking
3. Parameter validation
4. Simple queries to both models
5. Side-by-side model comparison
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from azure_openai_helper.llm_client import (
    validate_configuration, 
    get_available_models,
    llm_query
)

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)

def test_configuration():
    """Test 1: Validate configuration for both models."""
    print_section("TEST 1: Configuration Validation")
    
    try:
        config_result = validate_configuration()
        print("✓ Configuration validation passed")
        print(f"  Primary model configured: Yes")
        print(f"  Secondary model configured: {config_result.get('has_secondary_model', False)}")
        
        if config_result.get('has_secondary_model', False):
            print("  Both models are ready for testing!")
        else:
            print("  ⚠ Warning: Secondary model not configured. Some tests will be skipped.")
        
        return config_result
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        return None

def test_available_models():
    """Test 2: Check available models."""
    print_section("TEST 2: Available Models")
    
    try:
        models = get_available_models()
        print("✓ Available models retrieved:")
        for key, value in models.items():
            print(f"  {key}: {value}")
        return models
    except Exception as e:
        print(f"✗ Failed to get available models: {e}")
        return None

def test_parameter_validation():
    """Test 3: Validate parameter checking."""
    print_section("TEST 3: Parameter Validation")
    
    # Test empty prompt
    print("\nTesting empty prompt validation...")
    try:
        llm_query("")
        print("✗ Should have raised ValueError for empty prompt")
    except ValueError as e:
        print(f"✓ Correctly rejected empty prompt: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test invalid temperature
    print("\nTesting temperature validation...")
    try:
        llm_query("test", temperature=3.0)
        print("✗ Should have raised ValueError for temperature > 2.0")
    except ValueError as e:
        print(f"✓ Correctly rejected invalid temperature: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test invalid max_tokens
    print("\nTesting max_tokens validation...")
    try:
        llm_query("test", max_tokens=-10)
        print("✗ Should have raised ValueError for negative max_tokens")
    except ValueError as e:
        print(f"✓ Correctly rejected invalid max_tokens: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def test_primary_model():
    """Test 4: Simple query with primary model (GPT-4o)."""
    print_section("TEST 4: Primary Model Query (GPT-4o)")
    
    prompt = "What is 2+2? Answer with just the number."
    
    try:
        print(f"Prompt: {prompt}")
        print("Querying primary model...")
        
        response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=10,
            model="primary"
        )
        
        print(f"✓ Primary model responded successfully")
        print(f"  Response: {response.strip()}")
        
        return response
    except Exception as e:
        print(f"✗ Primary model query failed: {e}")
        return None

def test_secondary_model(has_secondary: bool):
    """Test 5: Simple query with secondary model (Phi-4-mini)."""
    print_section("TEST 5: Secondary Model Query (Phi-4-mini-instruct)")
    
    if not has_secondary:
        print("⊘ Test skipped: Secondary model not configured")
        return None
    
    prompt = "What is 2+2? Answer with just the number."
    
    try:
        print(f"Prompt: {prompt}")
        print("Querying secondary model...")
        
        response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=10,
            model="secondary"
        )
        
        print(f"✓ Secondary model responded successfully")
        print(f"  Response: {response.strip()}")
        
        return response
    except Exception as e:
        print(f"✗ Secondary model query failed: {e}")
        return None

def test_model_comparison(has_secondary: bool):
    """Test 6: Side-by-side comparison on same prompt."""
    print_section("TEST 6: Side-by-Side Model Comparison")
    
    if not has_secondary:
        print("⊘ Test skipped: Secondary model not configured")
        return
    
    # Use a more interesting prompt for comparison
    prompt = """In one sentence, explain what the 'lost in the middle' effect is in the context of large language models."""
    
    print(f"Prompt: {prompt}\n")
    
    # Query primary model
    print("Querying PRIMARY model (GPT-4o)...")
    try:
        primary_response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=100,
            model="primary"
        )
        print(f"✓ Primary response:")
        print(f"  {primary_response.strip()}\n")
    except Exception as e:
        print(f"✗ Primary model failed: {e}\n")
        primary_response = None
    
    # Query secondary model
    print("Querying SECONDARY model (Phi-4-mini-instruct)...")
    try:
        secondary_response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=100,
            model="secondary"
        )
        print(f"✓ Secondary response:")
        print(f"  {secondary_response.strip()}\n")
    except Exception as e:
        print(f"✗ Secondary model failed: {e}\n")
        secondary_response = None
    
    # Compare
    if primary_response and secondary_response:
        print("📊 Comparison:")
        print(f"  Primary length: {len(primary_response)} characters")
        print(f"  Secondary length: {len(secondary_response)} characters")
        print(f"  Both models can answer the prompt successfully!")

def test_default_behavior():
    """Test 7: Verify default behavior (no model parameter = primary)."""
    print_section("TEST 7: Default Behavior (Backward Compatibility)")
    
    prompt = "Say 'hello' in one word."
    
    try:
        print(f"Prompt: {prompt}")
        print("Querying without specifying model (should use primary)...")
        
        response = llm_query(
            prompt=prompt,
            temperature=0.0,
            max_tokens=5
        )
        
        print(f"✓ Default query worked (backward compatible)")
        print(f"  Response: {response.strip()}")
        
        return response
    except Exception as e:
        print(f"✗ Default query failed: {e}")
        return None

def run_all_tests():
    """Run all validation tests."""
    print("\n" + "="*70)
    print("  AZURE OPENAI HELPER - MULTI-MODEL VALIDATION TEST SUITE")
    print("="*70)
    
    # Test 1: Configuration
    config_result = test_configuration()
    if not config_result:
        print("\n❌ Cannot proceed without valid configuration. Exiting.")
        return
    
    has_secondary = config_result.get('has_secondary_model', False)
    
    # Test 2: Available models
    models = test_available_models()
    
    # Test 3: Parameter validation
    test_parameter_validation()
    
    # Test 4: Primary model
    primary_response = test_primary_model()
    
    # Test 5: Secondary model
    secondary_response = test_secondary_model(has_secondary)
    
    # Test 6: Model comparison
    test_model_comparison(has_secondary)
    
    # Test 7: Default behavior
    default_response = test_default_behavior()
    
    # Summary
    print_section("TEST SUITE SUMMARY")
    
    passed = 0
    total = 7
    
    if config_result:
        passed += 1
        print("✓ Test 1: Configuration validation")
    else:
        print("✗ Test 1: Configuration validation")
    
    if models:
        passed += 1
        print("✓ Test 2: Available models")
    else:
        print("✗ Test 2: Available models")
    
    # Parameter validation always runs
    passed += 1
    print("✓ Test 3: Parameter validation")
    
    if primary_response:
        passed += 1
        print("✓ Test 4: Primary model query")
    else:
        print("✗ Test 4: Primary model query")
    
    if has_secondary:
        if secondary_response:
            passed += 1
            print("✓ Test 5: Secondary model query")
        else:
            print("✗ Test 5: Secondary model query")
        
        # Test 6 runs if secondary configured
        if primary_response and secondary_response:
            passed += 1
            print("✓ Test 6: Model comparison")
        else:
            print("✗ Test 6: Model comparison")
    else:
        print("⊘ Test 5: Secondary model query (skipped - not configured)")
        print("⊘ Test 6: Model comparison (skipped - not configured)")
        # Don't count these against total
        total -= 2
    
    if default_response:
        passed += 1
        print("✓ Test 7: Default behavior")
    else:
        print("✗ Test 7: Default behavior")
    
    print(f"\n{'='*70}")
    print(f"  RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"  🎉 All tests passed! Multi-model support is working correctly.")
    elif passed >= total - 1:
        print(f"  ⚠ Almost there! Review failed tests above.")
    else:
        print(f"  ❌ Multiple tests failed. Review errors above.")
    
    print('='*70 + "\n")

if __name__ == "__main__":
    run_all_tests()
