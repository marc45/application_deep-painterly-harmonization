
comming soon 


# req 
	torch 
	
# some tips 
## * why daemon_gram.lua + daemon_gram.py  ,can you pls reduce into daemon_gram.lua just one file ? 
    ans : no ,I had tried some times like that 
        ```
            function call ()
                ...
                require "neural_gram.lua"
            end 
            while 1== 1 do 
                call()
                
            end 
        ```
        ```
        ERROR: class nn.ContentLoss has been already assigned a parent class nn
        ```
        - hance ,I have to wrap a compulsory ,persevering python_shell  


