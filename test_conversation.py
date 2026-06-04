from utils.conversation_tester import ConversationTester

tester = ConversationTester(max_turns=4)

# Test 1 — Simple resolution
print("=== Test 1: Simple Resolution ===")
result = tester.run_conversation([
    "My laptop is not turning on",
    "I already tried that, still not working",
    "The charging light is also not coming on"
])

print(f"Final Status: {result['final_status']}")
print(f"Total Turns: {result['total_turns']}")
for turn in result['turns']:
    print(f"\nTurn {turn['turn']}:")
    print(f"User: {turn['user']}")
    print(f"Response: {turn['response'][:200]}...")
    print(f"Escalated: {turn['escalated']}")

# Test 2 — Context retention
print("\n=== Test 2: Context Retention ===")
result2 = tester.run_conversation([
    "My name is Ranvir and I ordered a laptop",
    "What is my name and what did I order?"
])

print(f"Final Status: {result2['final_status']}")
for turn in result2['turns']:
    print(f"\nTurn {turn['turn']}:")
    print(f"User: {turn['user']}")
    print(f"Response: {turn['response'][:200]}...")