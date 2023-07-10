import 'dart:math';

import 'package:tuple/tuple.dart';

import 'package:vector_math/vector_math.dart';


double  calcAlt(List<double> H) {
  // ASSUMPTHION: we assume that the phone side rotation or around phone Z axis is ~ zero
  // calc alt
  double altitude = atan2(H[2], H[1]);

  // to degree
  altitude = altitude * 180 / pi;

  // we need to convet the sign of the angle because we want the Z axis out from the front of the phone not the back,
  // That is because the the gravty is pulling the screen of the phone not the back
  double newAlt = altitude * -1;
  print(newAlt);
  return  altitude;
}

Matrix3 makeTransformationMatrix3D(double theta) {
  // This function will create a transformation matrix from one Angle which is around X axis
  double cs = cos(theta * pi / 180.0);
  double sn = sin(theta * pi / 180.0);
  Matrix3 T = Matrix3.identity();
  T.setColumn(0, Vector3(1, 0, 0));
  T.setColumn(1, Vector3(0, cs, -sn));
  T.setColumn(2, Vector3(0, sn, cs));
  
//   indexing the array is vertical first then horz so if
//   x = [[0,3,6],
//        [1,4,7],
//        [2,5,8]]


  return T;
}


List<double> rotateFrame(double theta, List<double> frame) {
  // This function rotates the frame by the specified angle.
  Matrix3 R1 = makeTransformationMatrix3D(theta);
  List<double> rotatedFrame = [];
  for (int i = 0; i < 3; i++) {
    rotatedFrame.add(R1[i] * frame[0] + R1[i+3] * frame[ 1] + R1[i+6] * frame[2]);
  }
    
  return rotatedFrame;
}


List<double> inverseSign(List<double> list) {
  List<double> inversedList = [];
  for (int i = 0; i < list.length; i++) {
    inversedList.add(-list[i]);
  }

  return inversedList;
}


double getAzimuth(List<double> G_horz_fr_vec) {
  //   -> hor frame X         [[-34.          -0.          -0.        ]
  //   -> hor frame Y          [ -0.           4.5157124   11.89369003]
  //   -> hor frame Z          [ -0.         -33.69878843   1.59378085]]
  //                            ^mob fr X      ^mob fr Y     ^mob fr Z 

  // taking the magnitudes of XYZ of Hor Frame
  // print(G_horz_fr)
  print(G_horz_fr_vec);

  double azimuth = atan2(G_horz_fr_vec[0], G_horz_fr_vec[2]) * 180.0 / pi;

  if (azimuth < 0) {
    azimuth = 360 + azimuth;
  }

  return azimuth;
}



void main() {
  List<double> H = [-0.45, 8.85, -4.5];
  List<double> G =  [-29,-17.5,17] ;
  G= inverseSign(G);
var altitude = calcAlt(H);
  print(altitude);
 var G_horz_fr_vec = rotateFrame(altitude,G);
  print(G_horz_fr_vec);
 var Azimuth = getAzimuth(G_horz_fr_vec);
  print(Azimuth);
  

//   print(rotateFrame(altitude,[29,17.5,-17] )[1]);

}