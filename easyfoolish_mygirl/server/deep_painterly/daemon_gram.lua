--[[
 copy from 3rdparts/deep-painterly-harmonization/neural_gram.lua
--]]
require 'torch'
local cmd = torch.CmdLine()

-- Basic options
cmd:option('-style_image', 'examples/inputs/seated-nude.jpg', 'Style target image')
cmd:option('-content_image', 'examples/inputs/tubingen.jpg', 'Content target image')
cmd:option('-tmask_image', 'examples/inputs/t_mask.jpg', 'Content tight mask image')
cmd:option('-mask_image', 'examples/inputs/t_mask.jpg', 'Content loose mask image')
cmd:option('-image_size', 700, 'Maximum height / width of generated image')
cmd:option('-gpu', 0, 'Zero-indexed ID of the GPU to use; for CPU mode set -gpu = -1')

-- Optimization options
cmd:option('-content_weight', 5)
cmd:option('-style_weight', 100)
cmd:option('-tv_weight',   1e-3)
cmd:option('-num_iterations', 1000)
cmd:option('-normalize_gradients', false)
cmd:option('-init', 'image', 'random|image')
cmd:option('-optimizer', 'lbfgs', 'lbfgs|adam')
cmd:option('-learning_rate', 1e1)

-- Output options
cmd:option('-print_iter', 50)
cmd:option('-save_iter', 100)
cmd:option('-output_image', 'out.png')

-- Other options
cmd:option('-style_scale', 1.0)
cmd:option('-original_colors', 0)
cmd:option('-pooling', 'max', 'max|avg')
cmd:option('-proto_file', 'models/VGG_ILSVRC_19_layers_deploy.prototxt')
cmd:option('-model_file', 'models/VGG_ILSVRC_19_layers.caffemodel')
cmd:option('-backend', 'nn', 'nn|cudnn|clnn')
cmd:option('-cudnn_autotune', false)
cmd:option('-seed', 316)

cmd:option('-content_layers', 'relu4_1',                 'layers for content')
cmd:option('-style_layers',   'relu3_1,relu4_1,relu5_1', 'layers for style')
-- Patchmatch
cmd:option('-patchmatch_size', 3)

--[[
 end copy from 3rdparts/deep-painterly-harmonization/neural_gram.lua
--]]
--local params = cmd:parse()
--local params2 = cmd:parse()

local scaner = require("scan")


function call()
    local rt = scaner.run()
    cmd_list = {} 
    for  _,tbx in ipairs(rt) do 
        local params1 = cmd:parse(arg)
        for k,v in pairs(tbx.tb1) do 
            params1[k] =v 
        end 
        item ={}
        item["d1"] = params1
        table.insert(cmd_list,item)
    end



    local  script_gram  =require ("neural_gram")

    for _,pp in ipairs(cmd_list ) do 
        print (pp.d1)
        script_gram.main(pp.d1)
    end
end 


while 1==1 do 
    if pcall(foo) then
    end
end


