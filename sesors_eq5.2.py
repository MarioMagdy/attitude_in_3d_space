import numpy as np
import math

def mag(x):
    return math.sqrt(sum(i ** 2 for i in x))


Us = ['x','y','z']







def calc_alt(H):
    "ASSUMPTHION: we assume that the phone side rotation or around phone Z axis is ~ zero"
    # calc alt
    Altitude = np.arctan2(H[2],H[1])

    # to degree 
    Altitude = Altitude * 180/math.pi 

    #we need to convet the sign of the angle because we want the Z axis out from the front of the phone not the back, 
    #That is because the the gravty is pulling the screen of the phone not the back
    New_alt = Altitude*-1
    # print(New_alt)
    return New_alt,Altitude



def make_tran_mat_3d(theta,around_what_num):
    """This function will create a transformation matrix from one Angle"""
    cs= np.cos(theta* np.pi / 180.)
    sn = np.sin(theta* np.pi / 180.)
    # print('theta,cs,sn',theta,cs,sn)

    if around_what_num ==1: 
        T = np.array([[cs,0 ,sn ],[0,1,0],[-sn,0 ,cs ]])

    elif around_what_num ==0: 
        T = np.array([[1,0,0],[0,cs ,sn ],[0,-sn ,cs ]])

    elif around_what_num ==2: 
        T = np.array([[cs ,-sn,0 ],[sn ,cs,0 ],[0,0,1]])

    return T



def rotate_frame(theta,frame,axis,sum_up= False,T = False):
    R1 = make_tran_mat_3d(theta,axis)
    if T :
        R1 = R1.T
    frame_rotated = np.multiply(R1,frame)
    if sum_up :
        frame_rotated=np.sum(frame_rotated,axis=1)
    return frame_rotated



def get_azimuth(G_horz_fr):
    #   -> hor frame X         [[-34.          -0.          -0.        ]
    #   -> hor frame Y          [ -0.           4.5157124   11.89369003]
    #   -> hor frame Z          [ -0.         -33.69878843   1.59378085]]
    #                            ^mob fr X      ^mob fr Y     ^mob fr Z 


    # taking the magnitudes of XYZ of Hor Frame
    # print(G_horz_fr)
    G_horz_fr_vec = np.sum(G_horz_fr,axis=1)
    # print(G_horz_fr_vec)

    azimuth = np.arctan2(G_horz_fr_vec[0],G_horz_fr_vec[2]) *180.0 /np.pi

    if azimuth<0:
        azimuth= 360+azimuth

    return azimuth




def calc_tilt(H):
    "caclutates rotation around z axis"
    # calc alt

    mag_H_yz = mag(H[1:])


    
    around_z = np.arctan2(H[0],mag_H_yz)

    # to degree 
    around_z = around_z * 180/math.pi 

    if around_z<0 :
        around_z = 360- around_z

    # print(New_alt)
    return around_z




def get_alt_az(reading):
    # Steps to find the phone Azimuth
    # Get Altitude
    # Apply Transformation matirces to get the horizontal Frame, which means in this case Alt =0 tilt =0
    # find the angle between Z axis in the horizontal frame and The Magnetic vector of earth OR
    # find the Atan of the Z and X axes in horizontal frame 


    H = reading['H']
    G = reading['G']

    # the magnetic vector is inversed
    G = np.array(G)*-1

    ######################################################################################################
    ################################# getting the tilt ###################################################
    ######################################################################################################
 
    mag_H_yz = mag(H[1:])
    angle_from_Y_to_Wprojection_ZY= np.arctan2(H[2],H[1])  *180.0 /np.pi #### ALTITUDE 
    W = mag(H)
    tilt_angle = np.arctan2(H[0],mag_H_yz)  *180.0 /np.pi
    # print(angle_from_Y_to_Wprojection_ZY,tilt_angle)



    


    ######################## THE TILT ANGLE IS TRUE ########################
    #######################################################################################


    # H_no_tilt = rotate_frame(tilt_angle,H,axis = 2,sum_up=1,T=0)
    # H_no_alt_no_tilt = rotate_frame(tilt_angle,rotate_frame(angle_from_Y_to_Wprojection_ZY,H,axis = 0,sum_up=1,T=0),axis = 2,sum_up=1,T=0)


    G_no_alt= rotate_frame(angle_from_Y_to_Wprojection_ZY,G,axis = 0,sum_up=1,T=0)
    G_no_alt_no_sum= rotate_frame(angle_from_Y_to_Wprojection_ZY,G,axis = 0,sum_up=0,T=0)
    
    G_no_alt_no_tilt= rotate_frame(tilt_angle,G_no_alt,axis = 2,sum_up=0,T=0)

    old_az =get_azimuth(G_no_alt_no_sum)
    new_az = get_azimuth(G_no_alt_no_tilt)




    print(f"real_alt_estimate: {reading['real_alt_estimate']} \t Calculated :-> {angle_from_Y_to_Wprojection_ZY}, \n real_az: {reading['real_az']}  \t Calculated :-> {new_az},  \t Calculated :-> {old_az}, ")



    


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
            'G': [24,-13,43] },


            {'real_alt_estimate' : 'No idea',
          'real_az' : 331 ,
           'H': [-5.42,2.45,7.91],
            'G': [25.8,16.8,-19] },


            {'real_alt_estimate' : 'No idea',
          'real_az' : 331 ,
           'H': [2.55,9.5,.31],
            'G': [25.8,16.8,-19] },


            {'real_alt_estimate' : 20,
          'real_az' : 52 ,
           'H': [3.9,8.5,-3],
            'G': [25.8,16.8,-19] }
,

 {'real_alt_estimate' : 4,
          'real_az' : 346 ,
           'H': [5.25,8.23,-1],
            'G': [37,-30,-40] }
            ]

for ind,reading in enumerate(readings):
    print("Reading number : ", ind+1)
    get_alt_az(reading)
    print()