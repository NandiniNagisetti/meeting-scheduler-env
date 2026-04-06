from models import Action

class GreedyAgent:
    def act(self, state):
        request = state.current_request

        best_time = None
        best_score = -1e9

        # Try all possible start times
        for t in range(10):
            score = 0

            # Prefer earlier times
            score -= t * 0.1

            # Priority boost
            score += request.priority * 2

            # Preference bonus
            for p in request.participants:
                if t in p.preferred_times:
                    score += 1

            # Deadline penalty
            if t > request.deadline:
                score -= 5

            if score > best_score:
                best_score = score
                best_time = t

        if best_time is None:
            return Action(action_type="reject")

        return Action(action_type="schedule", start_time=best_time)
