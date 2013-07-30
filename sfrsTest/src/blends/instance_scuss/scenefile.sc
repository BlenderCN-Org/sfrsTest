image {
	resolution 576 324
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
	name "iplane"
	type diffuse
	diff 1 1 1 
}

/*
object {
	shader iplane
	type plane
	p 0 0 0
	n 0 0 1
}
*/

shader {
	name "unnamed"
	type diffuse
	diff 1 1 1
}

shader {
	name "Green.shader"
	type diffuse
	diff { "sRGB nonlinear" 0.483 0.800 0.000 }

}

/*
light {
	type point
	color { "sRGB nonlinear" 1.000 1.000 1.000 }
	power 749.999570847
	p 4.076245 1.005454 5.903862
}
*/

camera {
	type   pinhole
	eye   7.481132 -6.507640 5.343665
	target 6.826270 -5.896974 4.898420
	up		 -0.317370 0.312469 0.895343
	fov   49.1343426412 
	aspect 1.77777777778 
}
include "E:\Graphics\Works\testbuildsfor253\InstanceCheck\Instan.obj.sc"

include "E:\Graphics\Works\testbuildsfor253\InstanceCheck\ins_col.sc"
