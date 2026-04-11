# assignment_helper.py - Assignment Help System
"""
Helps students work through coding assignments step-by-step.

This module provides guided assistance without giving away answers.
Students learn by solving problems themselves with structured guidance.
"""

from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from prompts import ASSIGNMENT_HELP_SYSTEM, ASSIGNMENT_BREAKDOWN_PROMPT
from logger import log_info, log_student_action

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AssignmentHelper:
    """
    Guides students through coding assignments
    
    Features:
    - Breaks assignments into steps
    - Provides hints without spoiling
    - Tracks progress through steps
    - Generates learning summary at the end
    """
    
    def __init__(self, student_name="Student"):
        self.student_name = student_name
        self.current_assignment = None
        self.current_step = 0
        self.steps_completed = []
        self.conversation_history = []
        self.concepts_learned = []
    
    # ================================================================
    # ANALYZE ASSIGNMENT
    # ================================================================
    
    def analyze_assignment(self, assignment_text):
        """
        Break down an assignment into manageable steps
        
        Args:
            assignment_text (str): The full assignment question
        
        Returns:
            dict: Breakdown with steps, concepts, difficulty
        """
        
        log_student_action("Analyze Assignment", f"Length: {len(assignment_text)}")
        
        # Get AI to analyze and break down the assignment
        prompt = ASSIGNMENT_BREAKDOWN_PROMPT.format(
            assignment_text=assignment_text
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing coding assignments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3  # Lower temp for more consistent structure
            )
            
            content = response.choices[0].message.content
            
            # Clean up response (remove markdown if present)
            content = content.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            breakdown = json.loads(content)
            
            # Store the assignment
            self.current_assignment = {
                "text": assignment_text,
                "breakdown": breakdown,
                "started_at": None,
                "completed_at": None
            }
            
            self.current_step = 0
            self.steps_completed = []
            
            log_info(f"Assignment analyzed: {len(breakdown['steps'])} steps identified")
            
            return breakdown
        
        except json.JSONDecodeError as e:
            log_info(f"JSON parse error: {e}")
            # Fallback: return a simple structure
            return {
                "concepts_required": ["Unknown"],
                "difficulty_estimate": "medium",
                "steps": [
                    {"step_number": 1, "description": "Break down the problem", "hint": "Start by understanding what's being asked"}
                ],
                "learning_objectives": ["Problem solving"]
            }
        except Exception as e:
            log_info(f"Error analyzing assignment: {e}")
            return None
    
    # ================================================================
    # GUIDED HELP
    # ================================================================
    
    def get_guidance(self, student_message=""):
        """
        Get guidance for the current step
        
        Args:
            student_message (str): Student's question or current work
        
        Returns:
            str: Tutor's guidance
        """
        
        if not self.current_assignment:
            return "Please start by sharing your assignment question with me!"
        
        # Build context
        breakdown = self.current_assignment["breakdown"]
        total_steps = len(breakdown["steps"])
        current_step_info = breakdown["steps"][self.current_step] if self.current_step < total_steps else None
        
        # Build conversation context
        context = f"""
Assignment: {self.current_assignment['text']}

Total Steps: {total_steps}
Current Step: {self.current_step + 1}/{total_steps}

Step Details: {current_step_info['description'] if current_step_info else 'All steps completed!'}

Steps Completed So Far: {', '.join([f"Step {s}" for s in self.steps_completed]) if self.steps_completed else 'None yet'}
"""
        
        # Add to conversation history
        if student_message:
            self.conversation_history.append({
                "role": "user",
                "content": student_message
            })
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": ASSIGNMENT_HELP_SYSTEM + "\n\nCONTEXT:\n" + context},
            *self.conversation_history
        ]
        
        # Get guidance
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=400
            )
            
            guidance = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": guidance
            })
            
            return guidance
        
        except Exception as e:
            return f"Error getting guidance: {e}"
    
    def mark_step_complete(self, step_number):
        """Mark a step as completed"""
        if step_number not in self.steps_completed:
            self.steps_completed.append(step_number)
            self.current_step = min(self.current_step + 1, 
                                   len(self.current_assignment["breakdown"]["steps"]))
            log_info(f"Step {step_number} marked complete")
    
    def is_assignment_complete(self):
        """Check if all steps are done"""
        if not self.current_assignment:
            return False
        
        total_steps = len(self.current_assignment["breakdown"]["steps"])
        return len(self.steps_completed) >= total_steps
    
    # ================================================================
    # SUMMARY GENERATION
    # ================================================================
    
    def generate_summary(self):
        """
        Generate a comprehensive learning summary
        
        Returns:
            dict: Summary of what was learned
        """
        
        if not self.current_assignment:
            return {"error": "No assignment to summarize"}
        
        breakdown = self.current_assignment["breakdown"]
        
        # Build summary
        summary = {
            "assignment": self.current_assignment["text"][:100] + "..." if len(self.current_assignment["text"]) > 100 else self.current_assignment["text"],
            "status": "Completed ✓" if self.is_assignment_complete() else f"In Progress ({len(self.steps_completed)}/{len(breakdown['steps'])} steps)",
            "concepts_covered": breakdown["concepts_required"],
            "difficulty": breakdown["difficulty_estimate"],
            "steps_completed": len(self.steps_completed),
            "total_steps": len(breakdown["steps"]),
            "learning_objectives": breakdown["learning_objectives"],
            "key_takeaways": self._extract_key_takeaways(),
            "next_steps": self._suggest_next_steps()
        }
        
        return summary
    
    def _extract_key_takeaways(self):
        """Extract key learning points from the conversation"""
        
        # Look through conversation for learning moments
        takeaways = []
        
        if not self.current_assignment:
            return takeaways
        
        # Add concepts as takeaways
        concepts = self.current_assignment["breakdown"]["concepts_required"]
        for concept in concepts[:3]:  # Top 3
            takeaways.append(f"Understanding of {concept}")
        
        return takeaways
    
    def _suggest_next_steps(self):
        """Suggest what to practice next"""
        
        if not self.current_assignment:
            return []
        
        concepts = self.current_assignment["breakdown"]["concepts_required"]
        
        # Simple progression map
        next_topics = {
            "loops": ["nested loops", "loop control", "list comprehensions"],
            "functions": ["recursion", "lambda functions", "decorators"],
            "lists": ["list methods", "sorting", "filtering"],
            "dictionaries": ["dictionary methods", "JSON", "data structures"],
            "conditionals": ["complex conditions", "ternary operators", "switch statements"]
        }
        
        suggestions = []
        for concept in concepts:
            if concept in next_topics:
                suggestions.extend(next_topics[concept])
        
        return list(set(suggestions))[:3]  # Return top 3 unique suggestions
    
    def format_summary_for_display(self):
        """Format summary as readable text"""
        
        summary = self.generate_summary()
        
        if "error" in summary:
            return summary["error"]
        
        formatted = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ASSIGNMENT SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Assignment: {summary['assignment']}
Status: {summary['status']}
Difficulty: {summary['difficulty'].upper()}

Progress:
✓ Steps Completed: {summary['steps_completed']}/{summary['total_steps']}

Concepts Covered:
{chr(10).join(['✓ ' + concept for concept in summary['concepts_covered']])}

What You Learned:
{chr(10).join(['• ' + takeaway for takeaway in summary['key_takeaways']])}

Learning Objectives Achieved:
{chr(10).join(['✓ ' + obj for obj in summary['learning_objectives']])}

Recommended Next Steps:
{chr(10).join(['→ ' + step for step in summary['next_steps']])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Great work on this assignment! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        return formatted
    
    def reset(self):
        """Reset for a new assignment"""
        self.current_assignment = None
        self.current_step = 0
        self.steps_completed = []
        self.conversation_history = []


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    print("="*60)
    print("🎓 TESTING ASSIGNMENT HELPER")
    print("="*60)
    
    # Create helper
    helper = AssignmentHelper("Obianuju")
    
    # Sample assignment
    assignment = """
    Write a Python function called 'find_max' that takes a list of numbers 
    as input and returns the largest number in the list. 
    Handle the case where the list is empty by returning None.
    """
    
    print("\n📝 Assignment:")
    print(assignment)
    
    # Analyze
    print("\n🔍 Analyzing assignment...")
    breakdown = helper.analyze_assignment(assignment)
    
    print(f"\n✓ Breakdown:")
    print(f"  Difficulty: {breakdown['difficulty_estimate']}")
    print(f"  Concepts: {', '.join(breakdown['concepts_required'])}")
    print(f"  Steps: {len(breakdown['steps'])}")
    
    for step in breakdown['steps']:
        print(f"\n  Step {step['step_number']}: {step['description']}")
        print(f"    Hint: {step['hint']}")
    
    # Get initial guidance
    print("\n💬 Getting initial guidance...")
    guidance = helper.get_guidance("I'm ready to start!")
    print(f"\nTutor: {guidance[:200]}...")
    
    # Simulate completion
    print("\n✓ Marking steps complete...")
    for i in range(len(breakdown['steps'])):
        helper.mark_step_complete(i + 1)
    
    # Generate summary
    print("\n📊 Generating summary...")
    summary = helper.format_summary_for_display()
    print(summary)
    
    print("\n" + "="*60)
    print("✅ ASSIGNMENT HELPER TEST COMPLETE!")
    print("="*60)