### Description
Frontend test measures time of so called frontend transactions using Chromium browser. Frontend transaction is  e.g. 
period between click on search button until appearance of some frontend element representing finalized page with  
search results. In a log file `output.txt` the frontend transactions are delimited
by 

`Notify: Transaction "front-end transaction name" started` 

and

`Notify: Transaction "front-end transaction name" ended with a "Pass" status (Duration: 53.2710 Think Time: 1.0070 Wasted Time: 0.9600) ...`

### Task
   * Limit yourself only to frontend transaction containing HTTP `POST`s request   
		Achieved this by ignoring transactions with GET requests
   
   * Identify as many performance metrics as possible for the frontend transaction which can be retrieved from the log file.
		As only POST calls are considered , two performance metrics are identified:
		1. Average transaction response time (RT = Duration - Wasted time)
		2. Average request size
		
   * Performance metrics is any measure (frontend behaviour) that directly can influence user's perception of fast response and can be optimized either on frontend or backend.
		1. Response time is inversely proportional response perception , so is a strong performance metrics
		2. Request size helps user identifying the application responsiveness when subjected to high/low request inputs
   
   * Write a sample code (in your favorite language) for processing the log file.
       * The output should be in `json` format.
			Metrics_ddmm_HHMMSS.json is the output file
       * The output should contain only 2-3 selected performance metrics.
			Output contains 2 performance metrics for each POST transaction
       
### Motivation
The frontend test represents `Virtual User`. Once the application is optimized for single virtual users with the help 
of such a detailed log we can simulate concurrent load of different types of virtual users and measure the limits of the
application under more realistic load conditions.    

###Syntax:
python ParserTool.py
Input : please provide the input file path for analysis
Output: Metrics_ddmm_HHMMSS.json


  