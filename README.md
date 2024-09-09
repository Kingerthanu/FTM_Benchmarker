# FTM_Benchmarker
Python Script In Which Will Use A Provided openai API Key As Well As A Fine-Tuned Model ID To Create A Client Session. With Provided Unit-Test Questions With Expected Answers For The Fine-Tuned Model To Give, We Will Compare These Expected Answers With The Answers Actually Given By Our Fine-Tuned openai Model And Get A Percentage Similarity Score Between The Two Answers By Asking Another openai Session How Semantically, And Theoretically Similpar The Two Solutions Are. This Gives Us A Good Guage On The Fine-Tuned Model's Capability In Answering Problems Related To It's Field Of Expertise.

----------------------------------------------
<img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49">

**The Breakdown:**
  Before Running The Program 3 Specific Things Need To Be Done To Ensure Valid Benchmarking These Are: <br>
    &nbsp;1.) Provide fine_tune_id On Line 263. <br>
    &nbsp;2.) Provide An openai.api_key On Line 6. <br>
    &nbsp;3.) Provide A .json File In Which Follows The Style-Guideline (**Shown Below**), Filling In "question" And "expected_answer" For Each Question In Questions <br>

  The Stylization Of The Benchmarks Should Be As Follows, Provided In A .json:

    # You Don't Need "given_answer", "differences" or "similarity" As Will Be Generated During Runtime
    "questions": [
          {
            "question": "YOUR QUESTION",
            "expected_answer": "YOUR EXPECTED ANSWER (WHAT YOU WANT THE FINE-TUNED MODEL TO SAY)",
            "given_answer": "____",
            "similarity": ____,
            "differences": ____
          },
          {
            "question": "YOUR QUESTION",
            "expected_answer": "YOUR EXPECTED ANSWER (WHAT YOU WANT THE FINE-TUNED MODEL TO SAY)",
            "given_answer": "____",
            "similarity": ____,
            "differences": ____
          },
        ]

  After The 3 Preliminary Tasks Are Complete, You Can Run The Script. 

  When Running The Script We Will Start By Initially Finding The Actual Model ID Associated With The Fine-Tuned Model ID We Are Provided By openai When Fine-Tuning (**fine_tune_id**). If We Provided A Valid Fine-Tuned ID, We Will Then Dump The Contents Of Our "questions" (Benchmarks) To Be Done Out Into A Struct. To Then Evaluate Each "question" In Our Pulled From .json We Will Use Multi-Threading. This Is Achieved In **evaluate_benchmark(...)**; We Will Send Off A Worker Thread To Process An Individual Benchmarking Question Entry, This Allows Us To Process Many Benchmarks In Paralell Instead Of Sequentially Processing Questions.

  In The Worker Function (**process_question(...)**), It Will Be Given An Individual Benchmark And In Each One Of These, We Will Have A "question" And "expected_answer". Initially We Will Ask Our Fine-Tuned Model Our Question, Getting It's Response. From This Fine-Tuned Model's Response, We Will Then Compare It To The Solution We Expected To Get Thats Provided in "expected_answer". Using openai Again, We Ask The ChatGPT-4 Model To Compare And Give A Similarity Score Between These Two Answers Based Upon Theoretical And Semantic Relations--This Can Allow Us To Quickly Compare Our Differing Solutions And Recommend Changes To Our Model If Lacking In A Specific Subtopic In The Fine-Tuned Model's Informational Knowledge.

  After These Worker Threads Ask These Questions And Get Their Similarity Scores, We Will Then Add Them All Back Together In A List Struct. Now When Leaving **evaluate_benchmark(...)** We Return This List Struct Of All The Worker Threads' Answers And Can Inject This Back Into The .json Provided, Adding "given_answer" "similarity" And "differences" Now As Entries For Each Benchmark. Before The Process Ends We Will Also Quickly Print The Contents Of Each Benchmark Out, Outlining The Similarity Score And Reasoning For This Score In Terminal.

<img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49">

----------------------------------------------

<img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49">



**Features:**

  **Dynamic Sand Cell:**
  
  ![DEMO_SAND-ezgif com-video-to-gif-converter](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/b1678a97-1f79-4b0b-aa31-2ce74fe05780)



<img src="https://github.com/user-attachments/assets/2b421925-ca04-42d5-979a-8f7eca4061a1" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/2b421925-ca04-42d5-979a-8f7eca4061a1" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/2b421925-ca04-42d5-979a-8f7eca4061a1" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/2b421925-ca04-42d5-979a-8f7eca4061a1" alt="Cornstarch <3" width="55" height="49">
