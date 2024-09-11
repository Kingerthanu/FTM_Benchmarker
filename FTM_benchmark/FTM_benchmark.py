import openai
import json
import concurrent.futures

# Initialize The OpenAI Client With Your Specific API Key
openai.api_key = "_________"

'''

  Desc: Using openai, Will Request Their AI Model To Review 2 Answers To A Single Question. It Will Create A Floating-Point Percentage Similarity Score Based On Their Semantic And Conceptual Commonality.

  Preconditions:
    1.) expected_answer & given_answer Are Attempting To Answer The Same Question
    2.) expected_answer Is Inferred To Be The Control/Correct Answer
  
  Postconditions:
    1.) Will Return A Float From [0.0f, 100.0f] If A Solution Is Given From AI Model
    2.) Will Return -1.0f If AI Model Wasn't Able To Get A Comparison Score
    3.) Returned similarity_score Will Denote A Percentile (10.0f => 10%)

'''
def get_ai_similarity_score(expected_answer: str, given_answer: str) -> tuple:
  """
  Compare the two answers using AI and return both the similarity score and the reason for the score.

  Returns:
      similarity_score (float): The similarity score between 0.0 and 100.0.
      reason (str): The reason provided by the AI for the given score.
  """
  # Give openai Context On How We Will Compare Both Answers; We Utilize AI Model To Get Semantic And Theoretical Similarity Between Answers
  # Other Than General Word-Based Pattern Recognition
  prompt = f"""
  Compare the two answers below and provide a similarity score from 0.0 to 100.0 based on how semantically and conceptually similar they are 
  (your answer should come in this format with these TWO entries only; similarity_score= will be ONLY THE SCORE YOU GAVE IT; 
  REASON WILL BE EXPLAINING WHY YOU GAVE THAT SCORE):

  similarity_score=____
  reason=____

  <info>Expected Answer: {expected_answer}</info>

  <info>Given Answer: {given_answer}</info>
  """
  
  try:
    # Request AI to evaluate similarity and provide a reason
    response = openai.chat.completions.create(
      model="gpt-4o-mini-2024-07-18",
      messages=[
        {"role": "system", "content": "You are an expert at comparing technical answers in computer science and providing similarity scores."},
        {"role": "user", "content": prompt}
      ]
    )

    # Extract the response content, expecting the score and reason
    content = response.choices[0].message.content.strip()

    # Use simple string processing to extract the score and reason
    similarity_score = float(content.split("similarity_score=")[1].split("\n")[0].strip())
    reason = content.split("reason=")[1].strip()

    return (similarity_score, reason)
  except Exception as e:
    print(f"Error calculating AI similarity score: {e}")
    return -1.0, "Error: Unable to calculate similarity."


'''

  Desc: Will Grab The Fine-Tuned Model In Which Is Associated With The Provided Fine-Tune Model ID (fine_tune_id).

  Preconditions:
    1.) fine_tune_id Is A Hash/ID String In Which Points To A Fine-Tuned Model Hosted On openai
  
  Postconditions:
    1.) Will Return A String Of The Fine-Tuned Model If Able To Successfully Find The Model With fine_tune_id
    2.) Will Return None If Not Able To Successfully Retrieve The Fine-Tuned Model With The Provided fine_tune_id

'''
def retrieve_fine_tune(fine_tune_id: str) -> str:
  """Retrieves the fine-tuned model ID from a completed fine-tuning job."""
  try:
    # Ask openai For The Model We Used During This Fine-Tuning Job
    fine_tune_status = openai.fine_tuning.jobs.retrieve(fine_tune_id)

    # Check The Current State Of The Fine-Tuned Model (Complete, Not Valid, Etc.)
    status = fine_tune_status.status
    print(f"Fine-tune job status: {status}")

    # If Our Model Was Created, And Is Able To Be Talked To, Give Our ID For Client Communication
    if status == "succeeded":
      fine_tuned_model_id = fine_tune_status.fine_tuned_model
      print(f"Fine-tuning succeeded. Model ID: {fine_tuned_model_id}")
      return fine_tuned_model_id
    # Else If Our Model Has A Problem (Not Made, Issues In Retrieval) Don't Give The ID To Client
    elif status == "failed":
      print("Fine-tuning failed.")
      return None
    # Else If Another Error Code We Don't Expect, Just Blurt It To Client
    else:
      print(f"Unexpected status: {status}")
      return None
  except Exception as e:
    # If While Grabbing Our Model We Had An Outstanding Exception When Communicating To The API
    print(f"Error retrieving fine-tuned model: {e}")
    return None


'''

  Desc: Using openai, Give It Our Fine-Tuned Model ID In Order To Answer A Provided prompt Question, Returning The Answer.

  Preconditions:
    1.) prompt Is The Provided Question Being Asked To The Fine-Tuned Model
    2.) model_id Points To A Valid openai Model
  
  Postconditions:
    1.) Will Return A Float From [0.0f, 100.0f] If A Solution Is Given From AI Model
    2.) Return None If Error In Chat Creation With openai's API

'''
def test_fine_tuned_model(prompt: str, model_id: str) -> str:
  """Sends a prompt to the fine-tuned model and returns the response."""
  # Ask Our Fine-Tuned Model Our Prompt
  try:
    response = openai.chat.completions.create(
      model=model_id,
      messages=[
        {"role": "user", "content": prompt}
      ]
    )

    # Return The Answer Given To Our Prompt By Our Fine-Tuned Model
    answer = response.choices[0].message.content
    return answer
  # Else If We Had A Outstanding Exception When Communicating With The API
  except Exception as e:
    print(f"Error testing fine-tuned model: {e}")
    return None


'''

  Desc: Worker Thread Function In Which Will Ask A Passed openai Model (model_id) A Provided Question And Will Compare This Answer From This Model To A Known, Expected Answer; Using These Two 
  Answers To Find A Similarity Score Between The Two Using Another openai Request.

  Preconditions:
    1.) Each question Entry Contains AT LEAST A "question" and "expected_answer" In Order To Properly Compare (Infers User Already Pre-Defined Some Questions And Expected Answers To Test Model With)
    2.) model_id Points To A Valid Fine-Tuned Model Hosted On openai
    
  Postconditions:
    1.) Will Return A Dictionary Entry In Which Concatenates Our Fine-Tuned Model's Answer And It's Similarity With Our Expected Answer
    2.) Will Set Similarity Score To -1.0f If AI Model Wasn't Able To Get A Comparison Score

'''
def process_question(question: dict, model_id: str) -> dict:
  # Using Our Pre-Fetched Question And Expected Answer, Get An Answer Now From Our Fine-Tuned Model And Compare It's Correctness
  question_text = question["question"]
  expected_answer = question["expected_answer"]

  # Ask openai Fine-Tuned Model Our Question
  given_answer = test_fine_tuned_model(question_text, model_id)
  
  if given_answer:
    # If They Gave Us A Valid Answer, Now Compare It With Our Expected Answer
    similarity, reason = get_ai_similarity_score(expected_answer, given_answer)
  else:
    # If A Invalid Answer Was Given (I.E. Wrong Model ID, API Problems) Just Set The Similarity To -1.0 To Denote Not Computed
    similarity, reason = -1.0, "No valid answer given."

  # Package Up Our Result Into JSON
  result = {
    "question": question_text,
    "expected_answer": expected_answer,
    "given_answer": given_answer,
    "similarity": similarity,
    "differences": reason
  }

  return result


'''

  Desc: Use Multi-Threaded Processing In Order To Send Off Many Individual Workers To Process A Given Question (Get Fine-Tune Solution & Compare With Expected Solution) 
  All Together, Allowing For Parrellized Computations For Less Wait-Time.

  Preconditions:
    1.) model_id Points To A Valid openai Model
    2.) benchmark_data Is Formatted As Follows (You Don't Need "given_answer", "differences" or "similarity" As Will Be Generated During Runtime):
       "questions": [
        {
          "question": "____",
          "expected_answer": "____",
          "given_answer": "____",
          "similarity": ____,
          "differences": ____
        },
        {
          "question": "____",
          "expected_answer": "____",
          "given_answer": "____",
          "similarity": ____,
          "differences": ____
        },
      ]
        
  Postconditions:
    1.) Will Return A List Of Dictionary Entries For Each Question, Providing The Fine-Tuned Model Response As Well As It's Similarity With The Expected Solution
    2.) All Worker Threads Have Arrived Back Home After Send-Off
    
'''
def evaluate_benchmark(benchmark_data, model_id) -> list[dict]:
  # Using Multi-Threading, Send Off Worker Threads To Process Each Individual Question And Compare Its Similarity For Fast, Paralell Computations
  results = []
  
  # Set-Up Our Thread Manager
  with concurrent.futures.ThreadPoolExecutor() as executor:
    # For Each Question, Send Off A Helper
    futures = [executor.submit(process_question, q, model_id) for q in benchmark_data["questions"]]

    # If Our Current Thread Is Completed, Add It's Result Into Our Return Struct
    for future in concurrent.futures.as_completed(futures):
      results.append(future.result())

  # After Each Worker Has Computed It's Problem, Return All Computations In One Struct For Easy JSON Insertion
  return results


'''

  Desc: Using A Fine-Tuned Model And A Given JSON Structure In Below Format, Ask The Fine-Tuned Model A Question And Compare It With Our Expected Answer.
  Comparison Will Be Done With Another openai Session In Which Will Check For Semantic And Theoretical Similarities To Ensure The Two Answers Match Not Just Based
  On Word Usage, But Also On Topic Discussion.

  Preconditions:
    1.) fine_tune_id Points To A Valid openai Model
    2.) output_json_path's Contents Are Formatted As Follows (You Don't Need "given_answer", "differences" or "similarity" As Will Be Generated During Runtime):
       "questions": [
        {
          "question": "____",
          "expected_answer": "____",
          "given_answer": "____",
          "similarity": ____,
          "differences": ____
        },
        {
          "question": "____",
          "expected_answer": "____",
          "given_answer": "____",
          "similarity": ____,
          "differences": ____
        },
      ]
        
  Postconditions:
    1.) Will Save The List Of Dictionary Entries For Each Question, Providing The Fine-Tuned Model Response As Well As It's Similarity With The Expected Solution Back In The output_json_path
    
'''
if __name__ == "__main__":

  # Current Fine-Tuned Model ID
  fine_tune_id = "________"

  # Current File Path Of The .json Holding Our Benchmarks
  output_json_path = r"C:\Users\bensp\OneDrive\Programming File\The Code Box\Python Documents\OpenQQuantify\Boards\BOARD_Arduino_Mega_2560_Rev3-Benjamin\TrainingProcessing\UT_RISC-V_Optimization.json"

  # Retrieve The Fine-Tuning Job And Get The Fine-Tuned Model ID
  fine_tuned_model_id = retrieve_fine_tune(fine_tune_id)

  # If Failed Grabbing Our Model ID, Return Error
  if not fine_tuned_model_id:
    raise KeyError("Failed To Retrieve The Fine-Tuned Model ID :</ ...")

  # Load The Benchmark Questions And Answers
  with open(output_json_path, 'r') as f:
    benchmark_data = json.load(f)

  # Evaluate The Benchmark And Update Answers
  results = evaluate_benchmark(benchmark_data, fine_tuned_model_id)

  # Update Benchmark Data With New Answers
  benchmark_data["questions"] = results

  # Save The Updated Content To The Output JSON File
  with open(output_json_path, 'w', encoding='utf-8') as output_file:
    json.dump(benchmark_data, output_file, ensure_ascii=False, indent=2)

  print(f"Updated JSON saved to {output_json_path}")

  for indx, entry in enumerate(results):
    print(f"\nUnit-Test {indx + 1} Similarity Score: {entry['similarity']} \n"
          f"Reasoning: {entry['differences']}\n")


  input()
