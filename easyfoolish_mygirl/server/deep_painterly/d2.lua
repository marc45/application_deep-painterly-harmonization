require 'torch'

local cmd2 = torch.CmdLine()

-- Basic options
cmd2:option('-style_image', 'examples/inputs/seated-nude.jpg', 'Style target image')
cmd2:option('-content_image', 'examples/inputs/tubingen.jpg', 'Content target image')
cmd2:option('-cnnmrf_image', 'examples/inputs/cnnmrf.jpg', 'CNNMRF image')
cmd2:option('-tmask_image', 'examples/inputs/t_mask.jpg', 'Content tight mask image')
cmd2:option('-mask_image', 'examples/inputs/t_mask.jpg', 'Content loose mask image')
cmd2:option('-image_size', 700, 'Maximum height / width of generated image')
cmd2:option('-gpu', 0, 'Zero-indexed ID of the GPU to use; for CPU mode set -gpu = -1')

-- Optimization optins
cmd2:option('-init', 'image', 'random|image')
cmd2:option('-optimizer', 'lbfgs', 'lbfgs|adam')
cmd2:option('-learning_rate', 0.1)

-- Output options
cmd2:option('-print_iter', 50)
cmd2:option('-save_iter', 100)
cmd2:option('-index', 0)
cmd2:option('-output_image', 'out.png')

-- Other options
cmd2:option('-original_colors', 0)
cmd2:option('-pooling', 'max', 'max|avg')
cmd2:option('-proto_file', 'models/VGG_ILSVRC_19_layers_deploy.prototxt')
cmd2:option('-model_file', 'models/VGG_ILSVRC_19_layers.caffemodel')
cmd2:option('-backend', 'nn', 'nn|cudnn|clnn')
cmd2:option('-cudnn_autotune', false)
cmd2:option('-seed', 316)
cmd2:option('-num_iterations', 1000)

-- Patchmatch
cmd2:option('-patchmatch_size', 3)
-- RefineNNF 
cmd2:option('-refine_size', 5)
cmd2:option('-refine_iter', 1)
-- Ring 
cmd2:option('-ring_radius', 1) 
-- Wiki Art
cmd2:option('-wikiart_fn', 'wikiart_output.txt')



--local params = cmd:parse()
--local params2 = cmd:parse()

local scaner = require("scan")
local rt = scaner.run()


cmd_list = {} 
for  _,tbx in ipairs(rt) do 
    local params2 = cmd2:parse(arg)
    for k,v in pairs(tbx.tb2) do 
        params2[k] =v 
    end 
    item ={}
    item["d2"] = params2
    table.insert(cmd_list,item)
end



local  script_paint  =require ("neural_paint")

print (script_gram)
for _,pp in ipairs(cmd_list ) do 
    print (pp.d2)
    script_paint.main(pp.d2)
end



