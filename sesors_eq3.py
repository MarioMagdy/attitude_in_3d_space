import numpy as np
import math

def mag(x):
    return math.sqrt(sum(i ** 2 for i in x))


Us = ['x','y','z']


# the magnetic vector is inversed
inverse_G = lambda G: np.array(G)*-1




# print(G)
def calc_alt(H):
    "ASSUMPTHION: we assume that the phone side rotation or around phone Z axis is ~ zero"
    # calc alt
    Altitude = np.arctan2(H[2],H[1])

    # to degree 
    Altitude = Altitude * 180/math.pi 

    #we need to convet the sign of the angle because we want the Z axis out from the front of the phone not the back, 
    #That is because the the gravty is pulling the screen of the phone not the back
    New_alt = Altitude*-1
    print(New_alt)
    return New_alt,Altitude


def make_tran_mat_3d(theta,around_what_num):
    """This function will create a transformation matrix from one Angle"""
    cs= np.cos(theta* np.pi / 180.)
    sn = np.sin(theta* np.pi / 180.)
    # print('theta,cs,sn',theta,cs,sn)

    if around_what_num ==1: 
        T = np.array([[cs,0 ,-sn ],[0,1,0],[sn,0 ,cs ]])

    elif around_what_num ==0: 
        T = np.array([[1,0,0],[0,cs ,sn ],[0,-sn ,cs ]])

    elif around_what_num ==2: 
        T = np.array([[cs ,-sn,0 ],[sn ,cs,0 ],[0,0,1]])

    return T








# H_mob_fr = np.array([[H[0],0,0],[0,H[1],0],[0,0,H[2]]])
# def 
# G_mob_fr = np.array([[G[0],0,0],[0,G[1],0],[0,0,G[2]]])

def rotate_frame(theta,frame):
    R1 = make_tran_mat_3d(theta,0)
    frame_rotated = np.multiply(R1,frame)
    return frame_rotated

# print('\n',G_mob_fr)

def get_azimuth(G_horz_fr):
    # Steps to find the phone Azimuth
    # Get Altitude
    # Apply Transformation matirx to get the horizontal Frame, which means in this case Alt =0 
    # find the angle between Z axis in the horizontal frame and The Magnetic vector of earth OR
    # find the Atan of the Z and X axes in horizontal frame 


    #   -> hor frame X         [[-34.          -0.          -0.        ]
    #   -> hor frame Y          [ -0.           4.5157124   11.89369003]
    #   -> hor frame Z          [ -0.         -33.69878843   1.59378085]]
    #                            ^mob fr X      ^mob fr Y     ^mob fr Z 


    # taking the magnitudes of XYZ of Hor Frame
    G_horz_fr_vec = np.sum(G_horz_fr,axis=1)
    # print(G_horz_fr_vec)

    #ORRR
    G_horz_fr_vec2 = [mag(G_horz_fr[i,:])  for i in range(3)]
    # print(G_horz_fr_vec2)
    # ORRRR  WE NEED TO ADD THE SIGN TO THE MAG


    azimuth = np.arctan2(G_horz_fr_vec[0],G_horz_fr_vec[2]) *180.0 /np.pi
    # azimuth2 = np.arctan2(G_horz_fr_vec2[0],G_horz_fr_vec2[2])*180.0 /np.pi

    if azimuth<0:
        azimuth= 360+azimuth
    # print(azimuth,azimuth2)
    return azimuth
    # print(azimuth,azimuth2)


# get_azimuth(G,H)
# get_azimuth(G2,H2)





def get_alt_az(reading):
    H = reading['H']
    G = reading['G']

    G = inverse_G(G)
    new_alt,alt = calc_alt(H)
    # print(new_alt)

    G_horz_fr = rotate_frame(alt,G)
   
    
    
    az = get_azimuth(G_horz_fr)

    print(f"real_alt_estimate: {reading['real_alt_estimate']} \t Calculated :-> {new_alt}, \n real_az: {reading['real_az']}  \t Calculated :-> {az}")
    

    


readings= [{'real_alt_estimate' : 36,
          'real_az' : 52 ,
           'H': [-0.1,8.2,-5.61],
            'G': [-23.8,-28,7.8] }

            ,{'real_alt_estimate' : -15,
          'real_az' : 90 ,
           'H': [0.2,9.4,2.9],
            'G': [-34, -34.0,-12] },
            
            {'real_alt_estimate' : 25,
          'real_az' : 107 ,
           'H': [-0.45,8.85,-4.5],
            'G': [-29,-17.5,17] },

             


            {'real_alt_estimate' : 50,
          'real_az' : 233 ,
           'H': [-0.25,6,-7.8],
            'G': [24,-13,43] }
            
            ]

for ind,reading in enumerate(readings):
    print("Reading number : ", ind+1)
    get_alt_az(reading)
    print()