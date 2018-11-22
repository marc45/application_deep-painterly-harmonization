require 'paths'


local SCAN = {}

SCAN.scan_dir = "./listen/data_listen/"
SCAN.save_dir = "./listen/result_listen/"


function SCAN.file_exists (pathx)
    local flg =false
    if paths.filep('your_desired_file_path') then
        flg=true
    else
        flg=false
    end
    return flg
end 

-- Lua implementation of PHP scandir function
function SCAN.scanfolder(directory)
    if not directory then 
        return nil 
    end

    local i, t, popen = 0, {}, io.popen
    local pfile = popen('ls -a "'..directory..'"')
    for filename in pfile:lines() do
        i = i + 1
        t[i] = filename
    end
    pfile:close()
    return t
end

function SCAN.distill_table(d1)
--for k in next,l do l[k] = l[k]:gsub("#", "") end
    ret = {}
    for kk,k in ipairs(d1) do
        if string.find(k,"naive") then
            local sid = string.gsub(k,"_naive.jpg","")
            table.insert (ret,sid)
        end
     end

    for kk,k in ipairs(d1) do
        if string.find(k,"_final_res.jpg") then
            local sid = string.gsub(k,"_final_res.jpg","")
            table.insert (ret,sid)
        end
     end

    for kk,k in ipairs(d1) do
        if string.find(k,"_inter_res.jpg") then
            local sid = string.gsub(k,"_inter_res.jpg","")
            table.insert (ret,sid)
        end
     end
    return ret
end

--[[
function SCAN.difference(a,b)
    function _find(a, tbl)
        for _,a_ in ipairs(tbl) do if a_==a then return true end end
    end
    local ret = {}
    for _,a_ in ipairs(a) do
        if not _find(a_,b) then table.insert(ret, a_) end
    end
    return ret
end
--]]
--
function SCAN.build_cmd (dlist) 

    local function _build_cmd(msg_id,prefix,save_dir) 
        tb={}
        tb.content_image = prefix .. msg_id .. "_naive.jpg" 
        tb.style_image = prefix .. msg_id .. "_target.jpg"
        tb.tmask_image = prefix .. msg_id .. "_c_mask.jpg"
        tb.mask_image = prefix .. msg_id .. "_c_mask_dilated.jpg" 
        tb.original_colors = 0 
        tb.image_size = 700
        tb.output_image = SCAN.save_dir ..  msg_id .. "_inter_res.jpg"
        tb.save_iter = 0
        tb.print_iter =100 


        tb2 = {}
        for j,x in ipairs(tb) do tb2[j] = x end

        tb2.index = 0
        tb2.wikiart_fn = "data/wikiart_output.txt"
        tb2.cnnmrf_image = tb.output_image
        tb2. output_image = SCAN.save_dir ..  msg_id .. "_final_res.jpg"
        tb2.num_iterations = 1000
        tb2.content_image = prefix .. msg_id .. "_naive.jpg" 
        tb2.style_image = prefix .. msg_id .. "_target.jpg"
        tb2.tmask_image = prefix .. msg_id .. "_c_mask.jpg"
        tb2.mask_image = prefix .. msg_id .. "_c_mask_dilated.jpg" 


        local tb3 = SCAN.file_exists(tb.output_image)
        if tb3 then 
            return nil,tb2 
        end 
        return tb,tb2 
    end 

    cmd_list = {}
    for k,item in ipairs(dlist) do 
        tb1 ,tb2 ,tb3 = _build_cmd(item, SCAN.scan_dir,SCAN.save_dir)
        cmd_item = {}
        cmd_item.tb1 =tb1 
        cmd_item.tb2 =tb2 
        table.insert (cmd_list,cmd_item)
    end

    return cmd_list
end

function SCAN.run() 
    local function contains(table, val)
       for i=1,#table do
          if table[i] == val then 
             return true
          end
       end
       return false
    end

-- in 

    local d1 = SCAN.distill_table( SCAN.scanfolder(SCAN.scan_dir) )
-- out 
    local d2 = SCAN.distill_table( SCAN.scanfolder(SCAN.save_dir) )


    work_list = {}
    for _,ex in ipairs(d1) do 
        if  contains(d2,ex) == false then 
            table.insert(work_list,ex)
        end
    end


    local ret = SCAN.build_cmd(work_list)

    return ret

end



return SCAN
