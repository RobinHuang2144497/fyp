import json
from collections import defaultdict


def get_trading_advice(impact_counts):
    """Generate trading advice based on impact distribution (with probabilities)"""
    if not impact_counts:
        return "Recommendation: No action (No data)"

    total = sum(impact_counts.values())
    max_count = max(impact_counts.values())
    max_impacts = [impact for impact, count in impact_counts.items() if count == max_count]

    if len(max_impacts) > 1:
        return "Recommendation: No action (There are multiple top impacts)"

    dominant_impact = max_impacts[0]
    probability = (impact_counts[dominant_impact] / total) * 100

    if dominant_impact == '上涨':
        return f"Recommendation: Buy (Probability of rise: {probability:.2f}%)"
    elif dominant_impact == '下跌':
        return f"Recommendation: Sell (Probability of fall: {probability:.2f}%)"
    else:
        return f"Recommendation: No action (Sideways/Irrelevant, Probability: {probability:.2f}%)"


def evaluate_impact_accuracy(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = 0
    matches = 0
    output_impacts = defaultdict(int)
    impact1_counts = defaultdict(int)
    correct_up = 0
    correct_down = 0
    total_up = 0
    total_down = 0

    for item in data:

        try:
            human_impact = item["output"]["impact"]
            model_impact = item["impact1"]
        except KeyError as e:
            print(f"Data format error, missing required field: {e}")
            continue


        total += 1
        if human_impact == model_impact:
            matches += 1


        output_impacts[human_impact] += 1
        impact1_counts[model_impact] += 1


        if human_impact == '上涨':
            total_up += 1
            if model_impact == '上涨':
                correct_up += 1
        elif human_impact == '下跌':
            total_down += 1
            if model_impact == '下跌':
                correct_down += 1


    accuracy = (matches / total) * 100 if total > 0 else 0
    accuracy_up = (correct_up / total_up) * 100 if total_up > 0 else 0
    accuracy_down = (correct_down / total_down) * 100 if total_down > 0 else 0

    # Print basic statistics
    print(f"Total sample count: {total}")
    print(f"Matching count: {matches}")
    print(f"Accuracy: {accuracy:.2f}%\n")
    print(f"Accuracy for rise: {accuracy_up:.2f}%")
    #print(f"Accuracy for fall: {accuracy_down:.2f}%\n")

    # Print distribution statistics
    print("Human-labeled impact distribution:")
    for impact, count in output_impacts.items():
        print(f"{impact}: {count} times")


    print("\n=== Trading advice based on human labels ===")
    print(get_trading_advice(output_impacts))

    print("\nModel predicted impact1 distribution:")
    for impact, count in impact1_counts.items():
        print(f"{impact}: {count} times")

    print("\n=== Trading advice based on model predictions ===")
    print(get_trading_advice(impact1_counts))


# Run the evaluation with the specified JSON file
evaluate_impact_accuracy("2024-1-24 .json")
