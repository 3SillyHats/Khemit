import numpy

def checkCollision(tri, position, radius):

	#test if spheres intersect

	centre_spacing  = tri.centre - position
	centre_distance2 = centre_spacing.dot(centre_spacing)
	if(centre_distance2 > (radius + tri.radius) ** 2):
		#spheres do not intersect
		return None

	#test if planes intersect
	plane_distance = abs( (tri.centre-position).dot(tri.norm) )

	if plane_distance  > radius :
		#plane does not intersect
		return None



	proj = numpy.empty([3,2])

	v     = (position - tri.vertices[0])
	i_vec = v - tri.norm * v.dot(tri.norm)
	i_len = numpy.linalg.norm(i_vec)

	if i_len == 0:
		v = -plane_distance*tri.norm
		v_norm = numpy.linalg.norm(v)
	else:
		i     = i_vec / i_len
		j     = numpy.cross(i,tri.norm)

		proj[0] = [i_len,0]
		proj[1] = [i.dot(position - tri.vertices[1]),j.dot(position - tri.vertices[1])]
		proj[2] = [i.dot(position - tri.vertices[2]),j.dot(position - tri.vertices[2])]

		proj_radius2 = radius ** 2 - plane_distance ** 2

		displacement = checkCollision2d(proj,proj_radius2)

		if displacement is None:
			return None

		v = -plane_distance*tri.norm + displacement.dot(numpy.array([i,j]))
		v_norm = numpy.linalg.norm(v)

	if v_norm == 0:
		return tri.norm*(radius/2)

	p = ((v_norm - radius)/v_norm) * v

	return p

def checkCollision2d(tri,r2):
	#test if origin is inside triangle

	#A *[t,s] = v   => [t,s] = A^-1 v

	A = numpy.array([[tri[1][0]-tri[0][0],tri[2][0]-tri[0][0]],[tri[1][1]-tri[0][1],tri[2][1]-tri[0][1]]])
	v = numpy.array([-tri[0][0],-tri[0][1]])
	st = numpy.linalg.inv(A).dot(v)
	if 0 <= st[0] <= 1  and 0 <= st[1]  <= 1 and st[0] + st[1] <= 1:
		#origin must be within triangle
		return numpy.array([0,0])

	for start in xrange(3):
		end = (start + 1)%3
		edge_vector = tri[end] - tri[start]
		edge_norm = numpy.array([edge_vector[1],edge_vector[0]])/numpy.linalg.norm(edge_vector)
		
		closest_dist = tri[start].dot(edge_norm)
 
		sub_vector = closest_dist*edge_norm - tri[start]
		ratio = sub_vector[0]/edge_vector[0]

		if ratio <= 0:
			#start point is closest to centre
			if tri[start].dot(tri[start]) <= r2:
				return tri[start]

		if ratio >= 1:
			#end point is closest to centre
			if tri[end].dot(tri[end]) <= r2:
				return tri[end]

		if closest_dist**2 < r2:
			#edge intersects circle
			return closest_dist*edge_norm

	#No intersection
	return None