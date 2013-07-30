image {
	resolution 960 540
	aa -2 2
	samples 12
	filter blackman-harris
}

trace-depths {
	diff 4 
	refl 2 
	refr 6 
}

background {
	color { "sRGB nonlinear" 0.051 0.051 0.051 }
}


bucket 24 spiral

light {
  type sunsky
  up 0 0 1
  east 0 1 0
  sundir 1 -1 0.31
  turbidity 2
  samples 1
}

shader {
	name "unnamed"
	type diffuse
	diff 1 1 1
}

shader {
	name "white.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.800 0.800 0.800 }

}


shader {
	name "down.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.289 0.000 0.800 }

}


shader {
	name "up.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.000 0.528 0.800 }

}


shader {
	name "Material.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.228 0.800 0.092 }

}


shader {
	name "Material.002.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.800 0.182 0.000 }

}


shader {
	name "Material.001.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.000 0.241 0.800 }

}


light {
	type point
	color { "sRGB nonlinear" 1.000 1.000 1.000 }
	power 749.999570847
	p 4.076245 1.005454 5.903862
}

camera {
	type   pinhole
	eye   7.481132 -6.507640 5.343665
	target 6.826270 -5.896974 4.898420
	up		 -0.317370 0.312469 0.895343
	fov   49.1343426412 
	aspect 1.77777777778 
}
include "E:\Graphics\Works\testbuildsfor253\InstanceCheck\transformCheck_1.obj.sc"

instance {
        name Arrow_Test
        geometry Arrow
        transform {				
                translate  +2.0000   +0.0000   +2.0000
                rotatey    +90.0000
				
				%rotatez    +180.0000
				%rotatex    -0.0000	
                
                scaleu     +1.0000
                  }
        shaders 3
			"white.shader"
			"down.shader"
			"up.shader"
		modifiers 3
			"None"
			"None"
			"None"
         }
		 