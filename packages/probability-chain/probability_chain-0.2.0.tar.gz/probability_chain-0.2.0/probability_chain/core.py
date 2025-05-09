import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

class ProbabilityChain:
    COLORS = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
        "bold": "\033[1m"
    }

    def __init__(self, stages):
        self.stages = stages  # list of base probabilities

    def compute_partial_probability(self, values=None, target_stage='E'):
        """Compute product up to and including the target stage."""
        values = values or self.stages
        stop_idx = ord(target_stage.upper()) - ord('A') + 1
        p = 1.0
        for val in values[:stop_idx]:
            p *= val
        return p

    def marginal_value(self, index, target_stage='E'):
        stop_idx = ord(target_stage.upper()) - ord('A') + 1
        product = 1.0
        for i, val in enumerate(self.stages[:stop_idx]):
            if i != index:
                product *= val
        return product

    def expected_rolls(self, prob):
        return float('inf') if prob <= 0 else 1 / prob

    def to_percent(self, value, decimals=4):
        return f"{value * 100:.{decimals}f}%"

    def print_result(self, result, color="reset", target_stage='E'):
        col = self.COLORS.get(color, self.COLORS["reset"])
        RESET = self.COLORS["reset"]
        BOLD = self.COLORS["bold"]

        if result["type"] == "single":
            print(f"{col}--- Stage {result['adjustments'][0][0]} +{result['adjustments'][0][1]} (target: {target_stage}) ---{RESET}")
            print(f"Original P({target_stage}): {BOLD}{self.to_percent(result['original'])}{RESET} (Rolls ~{result['original_rolls']:,.0f})")
            print(f"{col}Increase: {self.to_percent(result['increase'])}{RESET}")
            print(f"New P({target_stage}): {BOLD}{self.to_percent(result['new'])}{RESET} (Rolls ~{result['new_rolls']:,.0f})")
            print(f"{col}------------------------------------{RESET}\n")
        else:
            adj_str = ", ".join(f"{s}+{d}" for s, d in result["adjustments"])
            print(f"{col}--- Adjustments: {adj_str} (target: {target_stage}) ---{RESET}")
            print(f"Original P({target_stage}): {BOLD}{self.to_percent(result['original'])}{RESET} (Rolls ~{result['original_rolls']:,.0f})")
            print(f"{col}Increase: {self.to_percent(result['increase'])}{RESET}")
            print(f"New P({target_stage}): {BOLD}{self.to_percent(result['new'])}{RESET} (Rolls ~{result['new_rolls']:,.0f})")
            print(f"{col}------------------------------------{RESET}\n")

    def compare(self, *test_sets, target_stage='E'):
        """Compare multiple adjustment sets with respect to a target stage."""
        from copy import deepcopy

        def evaluate_adjustments(adjustments):
            modified = deepcopy(self.stages)
            for stage, delta in adjustments:
                idx = ord(stage.upper()) - ord('A')
                modified[idx] += delta

            original = self.compute_partial_probability(target_stage=target_stage)
            new = self.compute_partial_probability(modified, target_stage=target_stage)
            increase = new - original

            return {
                "type": "multi" if len(adjustments) > 1 else "single",
                "adjustments": adjustments,
                "original": original,
                "new": new,
                "increase": increase,
                "original_rolls": self.expected_rolls(original),
                "new_rolls": self.expected_rolls(new)
            }

        results = []
        for test in test_sets:
            if isinstance(test[0], tuple):
                results.append(evaluate_adjustments(test))
            else:
                results.append(evaluate_adjustments([test]))

        sorted_results = sorted(results, key=lambda r: r["increase"], reverse=True)
        best = sorted_results[0]["increase"]
        worst = sorted_results[-1]["increase"]

        for r in results:
            if r["increase"] == best:
                color = "green"
            elif r["increase"] == worst:
                color = "red"
            else:
                color = "yellow"
            self.print_result(r, color, target_stage=target_stage)

        print(f"✅ Comparison Complete (target stage: {target_stage})\n")

    def simulate_optimal_allocation(self, total_budget=0.1, step=0.01, target_stage='E'):
        """Simulate incrementally allocating budget to the stage with the highest marginal value."""

        probs = deepcopy(self.stages)
        stage_names = [chr(65 + i) for i in range(len(probs))]
        target_index = ord(target_stage.upper()) - ord('A') + 1
        history = []
        allocations = [0.0 for _ in probs]
        steps = []

        num_steps = int(total_budget / step)
        for i in range(num_steps):
            marginals = []
            for j in range(len(probs)):
                if j < target_index and probs[j] < 1.0:
                    original_p = self.compute_partial_probability(probs, target_stage=target_stage)
                    temp_probs = deepcopy(probs)
                    temp_probs[j] = min(temp_probs[j] + step, 1.0)
                    new_p = self.compute_partial_probability(temp_probs, target_stage=target_stage)
                    marginals.append(new_p - original_p)
                else:
                    marginals.append(-1)  # Prevent allocation to maxed-out or out-of-scope stages

            best_index = np.argmax(marginals)
            probs[best_index] += step
            allocations[best_index] += step
            p = self.compute_partial_probability(values=probs, target_stage=target_stage)
            history.append((sum(probs) - sum(self.stages), p))
            steps.append((i + 1, stage_names[best_index], probs[best_index]))

        # Print out step-by-step allocation
        print(
            f"\n{self.COLORS['bold']}Step-by-Step Increment Allocation (Target Stage: {target_stage}):{self.COLORS['reset']}")
        for step_num, stage, new_value in steps:
            print(f"Step {step_num:>2}: Allocated {step:.4f} to Stage {stage} (New Value: {new_value:.4f})")
        print()

        # Print out final allocation summary
        print(f"{self.COLORS['bold']}Final Allocation Summary (Total Budget: {total_budget}):{self.COLORS['reset']}")
        for i, alloc in enumerate(allocations):
            if i < target_index:
                print(f"Stage {stage_names[i]}: +{alloc:.4f}")
        print()
        # Print out final probability values
        print(f"{self.COLORS['bold']}Final Probability Values:{self.COLORS['reset']}")
        for i, value in enumerate(probs):
            if i < target_index:
                print(f"Stage {stage_names[i]}: {value:.4f}")
        print()

        # Plotting the result
        x_vals = [x[0] * 100 for x in history]  # budget spent in %
        y_vals = [x[1] * 100 for x in history]  # probability as %

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, marker='o')
        plt.title(f"Optimal Incremental Allocation to Maximize P({target_stage})")
        plt.xlabel("Budget Spent (%)")
        plt.ylabel(f"Probability of Reaching {target_stage} (%)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        return steps

    def summarize_allocation(self, steps):
        from collections import defaultdict

        # Count allocations and track evolution
        stage_counts = defaultdict(int)
        stage_timelines = defaultdict(list)

        for step_num, stage, new_value in steps:
            stage_counts[stage] += 1
            stage_timelines[stage].append((step_num, round(new_value, 4)))

        sorted_stages = sorted(stage_counts.items(), key=lambda x: -x[1])
        most_favored = sorted_stages[0][0]
        most_favored_count = sorted_stages[0][1]

        print(f"\n{self.COLORS['bold']}Allocation Summary:{self.COLORS['reset']}")

        # Detect first stage to reach 0.5
        stage_first_0_5 = {}
        for stage, timeline in stage_timelines.items():
            for step_num, value in timeline:
                if value >= 0.5:
                    stage_first_0_5[stage] = step_num
                    break

        if stage_first_0_5:
            sorted_first = sorted(stage_first_0_5.items(), key=lambda x: x[1])
            print(f"🟢 Stage(s) reaching 0.5 earliest:")
            for stage, step in sorted_first:
                print(f"  - Stage {stage} reached 0.5 at step {step}")
            print()

        # Identify dominant phase
        first_stage = steps[0][1]
        dominant_run_length = 0
        for i in range(len(steps)):
            if steps[i][1] == first_stage:
                dominant_run_length += 1
            else:
                break

        print(f"📊 Stage {first_stage} dominated early allocation with {dominant_run_length} consecutive steps.")
        if most_favored_count > (len(steps) / len(self.stages)) * 1.2:
            print(f"🏆 Stage {most_favored} received more allocation than average ({most_favored_count} times).")
        else:
            print("🎯 Allocation was relatively balanced across stages.")

        print("\n🔄 Allocation Counts:")
        for stage, count in sorted(stage_counts.items()):
            print(f"  - Stage {stage}: {count} times")

        print("\n📈 Timeline Highlights:")
        for stage in sorted(stage_timelines.keys()):
            first_value = stage_timelines[stage][0][1]
            final_value = stage_timelines[stage][-1][1]
            print(f"  - Stage {stage}: from {first_value} → {final_value}")

        print()
