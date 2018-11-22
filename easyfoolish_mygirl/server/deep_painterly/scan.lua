require 'paths'


local SCAN = {}

SCAN.scan_dir = "./listen/data_listen/"
SCAN.save_dir = "./listen/result_listen/"

SCAN.data_wiki = "../../../3rdparts/deep-painterly-harmonization/"

function SCAN.file_exists (pathx)
    local flg =false
    if paths.filep(pathx) then
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
    local ret = {}
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

function SCAN.build_cmd (dlist) 

    local function deepcopy(orig)
        local orig_type = type(orig)
        local copy
        if orig_type == 'table' then
            copy = {}
            for orig_key, orig_value in next, orig, nil do
                copy[deepcopy(orig_key)] = deepcopy(orig_value)
            end
            setmetatable(copy, deepcopy(getmetatable(orig)))
        else -- number, string, boolean, etc
            copy = orig
        end
        return copy
    end

    local function _build_cmd(msg_id,prefix,save_dir) 

        tb={}
        tb. model_file = paths.concat(paths.cwd(), SCAN.data_wiki, "models/VGG_ILSVRC_19_layers.caffemodel" )
        tb. proto_file = paths.concat(paths.cwd(), SCAN.data_wiki, "models/VGG_ILSVRC_19_layers_deploy.prototxt" )

        tb.content_image = paths .concat(prefix, msg_id .. "_naive.jpg" )
        tb.style_image = paths .concat(prefix , msg_id .. "_target.jpg")
        tb.tmask_image = paths .concat(prefix, msg_id .. "_c_mask.jpg")
        tb.mask_image = paths .concat(prefix ,msg_id .. "_c_mask_dilated.jpg" )
        tb.original_colors = 0 
        tb.image_size = 700
        tb.output_image =  paths .concat( SCAN.save_dir ,  msg_id .. "_inter_res.jpg")
        tb.save_iter = 0
        tb.print_iter =100 


        tb2 = deepcopy(tb)
        --for j,x in ipairs(tb) do tb2[j] = x end

        tb2.index = 0
        --tb2.wikiart_fn = "data/wikiart_output.txt"
        tb2.wikiart_fn =paths.concat(paths.cwd(), SCAN.data_wiki,"data/wikiart_output.txt")
        tb2.cnnmrf_image = tb.output_image
        tb2. output_image = paths .concat( SCAN.save_dir ,  msg_id .. "_final_res.jpg" )
        tb2.num_iterations = 1000
--        tb2.content_image = paths .concat(prefix, msg_id .. "_naive.jpg" ) 
--        tb2.style_image = paths .concat(prefix, msg_id .. "_target.jpg" )
--        tb2.tmask_image = paths .concat(prefix, msg_id .. "_c_mask.jpg")
--        tb2.mask_image = paths .concat(prefix, msg_id .. "_c_mask_dilated.jpg" )


        local tb3 = SCAN.file_exists(tb.output_image)
        if tb3 then 
            return nil,tb2 
        end 
        return tb,tb2 
    end 

    cmd_list = {}
    for k,item in ipairs(dlist) do 
        tb1 ,tb2  = _build_cmd(item, SCAN.scan_dir,SCAN.save_dir)
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
    SCAN. scan_dir =paths .concat ( paths.cwd(SCAN.scan_dir) , SCAN.scan_dir)
    SCAN. save_dir =paths .concat ( paths.cwd(SCAN.save_dir) , SCAN.save_dir)
    local d1 = SCAN.distill_table( SCAN.scanfolder( SCAN.scan_dir ))
-- out 
    --local d3 = SCAN.distill_table( SCAN.scanfolder( SCAN.save_dir ))
    local d2 = {}
    local d3 = {}
    for i,item in ipairs(d1) do 
        local fn = item .. "_final_res.jpg"
        fn  =paths.concat( SCAN. save_dir , fn) 
        if  SCAN.file_exists(fn) ==false then 
            -- if inter exist  d3.append()
            -- else d2.append()
            --
            local fn1 = item .. "_inter_res.jpg"
            fn1  =paths.concat( SCAN. save_dir , fn1)

            if  SCAN.file_exists(fn1) == false then
                table.insert(d2,item)
            else
                table.insert(d3,item)
            end

        end
    end

    local ret3 = SCAN.build_cmd(d3)
    local ret2 = SCAN.build_cmd(d2)

    local ret3 = SCAN.shuffle(ret3)
    local ret2 = SCAN.shuffle(ret2)

    return ret2,ret3

end


function SCAN.shuffle(tbl)
  for i = #tbl, 1, -1 do
    local j = math.random(i)
    tbl[i], tbl[j] = tbl[j], tbl[i]
  end
  return tbl
end

return SCAN
