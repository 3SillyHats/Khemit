from numpy import *

class Triangle(object):
    def __init__(self, vertices):
        self.vertices = vertices
        self.norm = cross(vertices[1] - vertices[0], vertices[2] - vertices[0])
        if linalg.norm(self.norm) > 0:
            self.norm = self.norm / linalg.norm(self.norm)

        self.centre = average(vertices, axis=0)
        self.radius = max(
            linalg.norm(vertices[0] - self.centre),
            linalg.norm(vertices[1] - self.centre),
            linalg.norm(vertices[2] - self.centre),
        )

    def collideSphere(self, position, radius):
        #test if spheres intersect

        centre_spacing  = self.centre - position
        centre_distance2 = centre_spacing.dot(centre_spacing)
        if(centre_distance2 > (radius + self.radius) ** 2):
            #spheres do not intersect
            return None

    	#test if planes intersect
    	plane_distance = abs( (self.vertices[0]-position).dot(self.norm) )

        if plane_distance  > radius :
            #plane does not intersect
            return None

    	proj = empty([3,2])

    	v     = (position - self.vertices[0])
    	i_vec = v - self.norm * v.dot(self.norm)
    	i_len = linalg.norm(i_vec)

    	if i_len == 0:
            v = -plane_distance*self.norm
            v_norm = linalg.norm(v)
	else:
            i     = i_vec / i_len
            j     = cross(i,self.norm)

            proj[0] = [i_len,0]
            proj[1] = [i.dot(position - self.vertices[1]),j.dot(position - self.vertices[1])]
            proj[2] = [i.dot(position - self.vertices[2]),j.dot(position - self.vertices[2])]
            
            proj_radius2 = radius ** 2 - plane_distance ** 2
            
            displacement = self.checkCollision2d(proj,proj_radius2)
            
            if displacement is None:
                return None
                
            v = -plane_distance*self.norm + displacement.dot(array([i,j]))
            v_norm = linalg.norm(v)

        if v_norm == 0:
            print(self.norm)
            return self.norm*(radius/2)

        p = ((v_norm - radius)/v_norm) * v

    	return p

    def checkCollision2d(self,tri,r2):
        #test if origin is inside triangle
        
        #A *[t,s] = v   => [t,s] = A^-1 v
    
        A = array([[tri[1][0]-tri[0][0],tri[2][0]-tri[0][0]],[tri[1][1]-tri[0][1],tri[2][1]-tri[0][1]]])
        v = array([-tri[0][0],-tri[0][1]])

        if linalg.det(A) != 0:
            st = linalg.inv(A).dot(v)
            if 0 <= st[0] <= 1  and 0 <= st[1]  <= 1 and st[0] + st[1] <= 1:
                #origin must be within triangle
                return array([0,0])
        
        for start in xrange(3):
            end = (start + 1)%3
            edge_vector = tri[end] - tri[start]
            edge_norm = array([edge_vector[1],edge_vector[0]])/linalg.norm(edge_vector)
            
            closest_dist = tri[start].dot(edge_norm)
            
            sub_vector = closest_dist*edge_norm - tri[start]
            ratio = sub_vector[0]/edge_vector[0]
            
            if ratio <= 0:
                #start point is closest to centre
                if tri[start].dot(tri[start]) <= r2:
                    return tri[start]
                    
            elif ratio >= 1:
                #end point is closest to centre
                if tri[end].dot(tri[end]) <= r2:
                    return tri[end]

            elif closest_dist**2 < r2:
                #edge intersects circle
                return closest_dist*edge_norm

    	#No intersection
    	return None

def collide(x, r, triangles):
    dx = array([0,0,0],'f')
    
    penetrations = [
        #[1,array([0,0,1],'f')],
        #[0.5,array([0,0.5,0],'f')],
    ]
    for t in triangles:
        pen = t.collideSphere(x, r)
        if pen is not None:
            pen_depth = linalg.norm(pen)
            if pen_depth > 0:
                penetrations.append([pen_depth, pen/pen_depth])

    if len(penetrations) > 0:
        for i in xrange(20):
            penetrations.sort(key=lambda x: -x[0])
            if penetrations[0][0] <= 0:
                break
            dx += penetrations[0][0] * penetrations[0][1]
            for pen in penetrations:
                pen[0] -= (penetrations[0][0] * penetrations[0][1]).dot(pen[1])

    return dx
