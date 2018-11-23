
package.path=package.path .. ";../../../3rdparts/deep-painterly-harmonization/?.lua;" 
package.cpath=package.cpath .. ";../../../3rdparts/deep-painterly-harmonization/?.so;" 



--local params = cmd:parse()
--local params2 = cmd:parse()

local scaner = require("scan")


function call()
    local rt = ""
    rt,_ = scaner.run()
    cmd_list = {} 
    for  _,tbx in ipairs(rt) do 
        local params1 = tbx.tb1 
        table.insert(cmd_list,params1)


        break
    end
    if cmd_list then
        if table.getn(cmd_list)==0 then 
            return 
        end
    end

    argx ={}
    for old_i ,pp in pairs(arg) do 
        if old_i<=0 then 
            argx[old_i]=pp
        end
    end
    for i,pp in ipairs(cmd_list ) do 
        for k ,v in pairs(pp) do 
            table.insert(argx,"-"..k)
            table.insert(argx,v)
        end
    end

    arg = argx


    package.loaded[ 'neural_gram' ] = nil
    require "neural_gram"
end 



while 1==1 do 
    if pcall(call) then
    end
end




