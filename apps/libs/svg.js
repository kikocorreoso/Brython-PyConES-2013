$module = (function(){

$svgNS = "http://www.w3.org/2000/svg"
$xlinkNS = "http://www.w3.org/1999/xlink"

function $SVGTag(tag_name,args){
    // represents an SVG tag
    var $i = null
    var $obj = this
    var obj = $DOMNode(document.createElementNS($svgNS,tag_name))
    if(args!=undefined && args.length>0){
        $start = 0
        $first = args[0]
        // if first argument is not a keyword, it's the tag content
        if($first.__class__!==$Kw){
            $start = 1
            if(isinstance($first,[str,int,float])){
                txt = document.createTextNode(str($first))
                obj.elt.appendChild(txt)
            } else if($first.__class__===$TagSumDict){
                for($i=0;$i<$first.children.length;$i++){
                    obj.elt.appendChild($first.children[$i])
                }
            } else {
                try{obj.elt.appendChild($first.elt)}
                catch(err){$raise('ValueError','wrong element '+$first)}
            }
        }
        // attributes
        for($i=$start;$i<args.length;$i++){
            // keyword arguments
            $arg = args[$i]
            if($arg && $arg.__class__===$Kw){
                if($arg.name.toLowerCase().substr(0,2)=="on"){ // events
                    eval('DOMNode.bind(obj,"'+$arg.name.toLowerCase().substr(2)+'",function(){'+$arg.value+'})')
                }else if($arg.name.toLowerCase()=="style"){
                    DOMNode.set_style(obj,$arg.value)
                }else if($arg.name.toLowerCase().indexOf("href") !== -1){ // xlink:href
                    obj.elt.setAttributeNS( "http://www.w3.org/1999/xlink","href",$arg.value)
                } else {
                    if($arg.value!==false){
                        // option.selected=false sets it to true :-)
                        obj.elt.setAttributeNS(null,$arg.name.replace('_','-'),$arg.value)
                    }
                }
            }
        }
    }
    return obj
}

// SVG
var $svg_tags = ['a',
'altGlyph',
'altGlyphDef',
'altGlyphItem',
'animate',
'animateColor',
'animateMotion',
'animateTransform',
'circle',
'clipPath',
'color_profile', // instead of color-profile
'cursor',
'defs',
'desc',
'ellipse',
'feBlend',
'g',
'image',
'line',
'linearGradient',
'marker',
'mask',
'path',
'pattern',
'polygon',
'polyline',
'radialGradient',
'rect',
'stop',
'svg',
'text',
'tref',
'tspan',
'use']

$svg = function(){return $SVGTag('X',arguments)}
$svg += '' // source code

var obj = new Object()
for(var i=0;i<$svg_tags.length;i++){
    var tag = $svg_tags[i]
    eval('obj.'+tag+'='+$svg.replace('X',tag))
}
obj.__getattr__ = function(attr){return this[attr]}
return obj
})()