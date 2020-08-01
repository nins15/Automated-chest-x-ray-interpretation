# Automated chest x-ray interpretation:Project review
* Created a CNN model for detecting 5 diseases which are Cardiomegaly,Edema,Consolidation,Atelectasis,Pleural Effusion
* Removed the redundant parts from the image like shoulder or text using a library that can detect lungs on chest x-rays
* Mapped the uncertain values in the csv using LSR(Label smoothning regression).
* Trained a number of CNN models on all the images like XceptionNet, EfficientNet, InceptionResNetV2, DenseNet etc. to identify multiple labels for each class.
* Three models with best AUC were chosen for ensembelling by concatinating the last layers of each model.
