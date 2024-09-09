# FTM_Benchmarker
Python Script In Which Will Use A Provided openai API Key As Well As A Fine-Tuned Model ID To Create A Client Session. With Provided Unit-Test Questions With Expected Answers For The Fine-Tuned Model To Give, We Will Compare These Expected Answers With The Answers Actually Given By Our Fine-Tuned openai Model And Get A Percentage Similarity Score Between The Two Answers By Asking Another openai Session How Semantically, And Theoretically Similpar The Two Solutions Are. This Gives Us A Good Guage On The Fine-Tuned Model's Capability In Answering Problems Related To It's Field Of Expertise.

----------------------------------------------
<img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/c0ddb715-8ee3-4baf-b7bd-d0e904143eaf" alt="Cornstarch <3" width="55" height="49">

**The Breakdown:**

  Visually Speaking, The Program Revolves Around Class Hierachies In Practical Modulastic Design. Using OpenGL We Are Creating **X** Cubes Across Our Window For Each The X and Y Axis (This Will Give Us A Equally Sized 2D Array). These Cube Vertexes and Ways Of Stepping / Drawing Them Are Supplied To A Single Vertex Buffer, Indice Buffer, as Well As Vertex Array To Work With Buffer Traversals. 
  
  Physically Speaking, This Program Starts From The Root Parent Of A Dynamic_Cell. A Dynamic Cell Is A Wrapper For The Visual Cube "Cell" Being Drawn By OpenGL. Each Dynamic_Cell Will Be Given Its Starting Offset In The Single Vertex Buffer. This Will Allow Us To Call Unique Overrides On Our Visual Vertexes For Varying Cell Types. We Also Will Have A Supplied typeID For Utilization In Collision Type Callbacks As Unique Cell Types Will React Differently To Other Cell Types. Our Dynamic_Cell Will Also Have A Virtual Update Function As Well As React Function, This Allows Us To Override Our Subclasses Reactions While Still Providing A Shared Interface To Utilize Externally In Our World Space With Physics Reactions.

  Our Dynamic_Cells Are Encapsulated Inside A Map Object In Which Will Work As A Dainty Interface With Our World, Allowing Explosions In Our World Space, As Well As Other Unique Functionality Like Drawing Circles. 
  
  Dynamic_Cells Can Also Be Controlled By Dynamic_Entities Which Work To Inject Unique Behaiovor Onto A Bundle Of Dynamic_Cells. Currently We Have This Applied With Boulders And Rocks Which Are Simply Our Solid Stone Dynamic Cell Type In Which Are Controlled Now By The Entity. In A Unique Case We Have Applied Explosives As Well Which Work With Their Own Unique Bombaclat Cell Type Which Works As A Unique Dynamic Cell In The World While Still Having Their Lifetime Tightly Coupled With Its Entity Representation Of These Cells.

  We Also Included A UI Interface To Allow The User To Toggle Between Differing Spawn Types Within Our World Space Using Buttons With Collision Detection As Well As Sliders To Allow Varying Radiuses To Be Drawn When Spawning Circles Of A Given Cell Type.


  Because The Cells Work With A Reaction Function It Has To Be Checking Around It In The 2D-Cell Map. At Every Cycle Of The Main Loop, From The Bottom Row, From Left To Right We Will Tell Each Cell To "React" To Its Surroundings. This Will Proceed From The Lowest Row Of Hexagons All The Way Up To The Top, Starting At Each Row From The Left-Most Hexagon. This Is Very Important In The Update Routine As To Cutdown On Runtime As Well As Space Complexity (Also Because I Like Making Myself Suffer And Learning The Hard Way) I Updated Each Cell In-Place In The 2D-Cell Map.

Updating The Cells In-Place Means That Right After Executing Their React Function And Dying Or Becoming Alive The Cell Will Update Its State. This Isn't A Major Error And In Many Automatas I've Made It's Been There But Also Gives Some Depth To The Design As What This Bug/Feature Can Do Is Lets Say We Have A Drop Of Water Represented As One Of Our Hexagons:

If This Water Was To Flow From Right -> Left, Represented By Turning Off One Hexagon In The 2D-CellMap And Turning On THe Hexagon To The Left Of It.

Because We Are Our 2D-Array In Which We Are Indexing And Calling Each Reaction Of A Given Cell We Will Index from:

0 -> ROW_SIZE (Could Be Any Axis, Usually Are Moving Along One Direction Never Anti-Paralell)

Because Of This, If We Update A Water Cell At CELL_MAP[Index] And At This Cell We Will Flow Left We Basically Are Telling CELL_MAP[Index - 1] To Now Become A Water Cell While Telling Our Cell (CELL_MAP[Index] To Delete Its Reference To Being A Water Cell).

In This Case We Get Expected Behaivor As When We Update A Cell Behind Us We Don't Call Its React Until We Cycle This For-Loop Again (In Our Main Loop) This Means Every Tick Of The Game Loop Will Match Up With The Execution Tick Cycle Of Each Cells Reactions To Avoid Maybe Two Reaction Ticks Per Cycle.

In The Case Where This Becomes Bad Is When The Water Cell Wants To Move Right, Paralell To The Way We Are "Scanning" Our 2D-Map. This Is Because Unlike The Other Case Where CELL_MAP[Index - 1] Is Forced TO Be A Cell BEHIND The Current Main Loop Reaction For THis Tick, We Instead Update CELL_MAP[Index + 1] Which Is The Cell In Front Of Us Which Causes Us To Then Accidentally Update The Cell Infront Of Us In Which We Are Currently Checking. This Causes Problems As Now Next Cell React Call Will Be At Index++ Which Will Be At Index + 1. So We Basically Cause A Compounding Effect, As Without Any Flags We Will Now Treat This Cell As A Fresh Water Cell To Be Checked THIS SAME Main Loop Cycle. This Will Then Update CELL_MAP[Index+1]. This Will Keep Going Until We Hit A Wall So On The Right Side We Will Hit The Wall In One Check Of This Row While On The Left Side We Would've Only Moved One Cell. So Instead Of Taking Multiple Cycles To Move In The Rightward Direction Like It Does In The Leftward, We Are Basically Rushing Our Town Hall.

<img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/f6bece3c-7e19-44d0-9b24-426cb4e081c0" alt="Cornstarch <3" width="55" height="49">

----------------------------------------------

<img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49"> <img src="https://github.com/user-attachments/assets/d72f209b-a4ae-4d77-87f2-9b5316e7f97a" alt="Cornstarch <3" width="55" height="49">



**Features:**

  **Dynamic Sand Cell:**
  
  ![DEMO_SAND-ezgif com-video-to-gif-converter](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/b1678a97-1f79-4b0b-aa31-2ce74fe05780)


  **Dynamic Water Cell:**

  ![DEMO_WATER_TRICKLE-ezgif com-optimize](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/6e78370c-c6d5-437e-8883-f0885f2e2ef2)

  ![DEmo_WATER_BUILDUP-ezgif com-video-to-gif-converter](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/60177422-244f-4ad9-a71e-7830d890170d)


   **Dynamic Smoke Cell:**
  
   ![DEMO_SMOKE-ezgif com-optimize](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/7a770164-0437-448d-8ace-26440ebfc7eb)


   **Dynamic Flame Cell:**
  
   ![DEMO_FLAME_TWO-ezgif com-optimize](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/e5f9a408-f10f-4a27-9def-90a75437000e)

   ![DEMO_FLAME_ONE-ezgif com-optimize (1)](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4614a5b7-f445-431e-837f-dbfeb8d0f863)

  
  **Dynamic Bomb Entity:**

  ![DEMO_EXPLOSION-ezgif com-optimize](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/db105da4-6c27-4570-ae2a-18798d0310af)


  **Dynamic Boulder & Rock Entities:**

  ![DEMO_BOULDER-ezgif com-video-to-gif-converter](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4571385c-26ec-4b74-a528-e2c631e439ae)

  ![DEMO_BOULDER_GENERAL-ezgif com-video-to-gif-converter](https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4910bdc4-2af5-47e1-8586-4673ce321f5c)



<img src="https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4f7f141e-829e-43a9-b061-77e5cdf068bc" alt="Cornstarch <3" width="55" height="49"><img src="https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4f7f141e-829e-43a9-b061-77e5cdf068bc" alt="Cornstarch <3" width="55" height="49"><img src="https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4f7f141e-829e-43a9-b061-77e5cdf068bc" alt="Cornstarch <3" width="55" height="49"><img src="https://github.com/Kingerthanu/CPP_FallingSand/assets/76754592/4f7f141e-829e-43a9-b061-77e5cdf068bc" alt="Cornstarch <3" width="55" height="49">
