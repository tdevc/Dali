import RobotRun as rr
import numpy as np
import cv2

#==============================================================================================================    
def VideoFrameProcessingSimple():
    VF={"Format":"YUY2", "Resolution":"640x480", "FrameRate":30.0}
    #VF={"Format":"MJPG", "Resolution":"1920x1080", "FrameRate":30.0}
    rr.PreviewStart(VF)
    print("IsPreviewing="+str(rr.IsPreviewing()))
    i=0
    cf=rr.CVideoFrame() # create video frame instance to handle "negative video frame"
    cfCrop=rr.CVideoFrame() # create video frame instance to handle "croping video frame"
    cfFreq=rr.CVideoFrame() # Frequency video"

    while True:
        FrameSource=rr.VideoFrameGet("")
        FrameNegative=255-FrameSource;
        cf.VideoFrameSet(FrameSource)

        x1=40; y1=200; x2=600; y2=300
        P1=(x1,y1)
        P2=(x2,y2)
        PixelValue = FrameSource[y1,x1]
        #print(PixelValue[2],PixelValue[1],PixelValue[0])
        FrameCrop=cf.Crop(P1, P2).copy()
        #cf.Rectangle(P1, P2)
        #cv2.putText(FrameSource, 'asd',(x1,y1), cv2.FONT_HERSHEY_DUPLEX,0.5, (0, 255, 0), 1, cv2.LINE_AA)
        
        FrameFreq=np.fft.fft2(FrameCrop)
        FrameFreq=np.abs(FrameFreq)
        cfCrop.VideoFrameSet(FrameCrop)
        cfFreq.VideoFrameSet(FrameFreq)
        #[Show all video windows]==========================================
        cf.VideoShow('Negative Video')
        cfCrop.VideoShow('Crop Video')
        cfFreq.VideoShow('Magnitude Spectrum(2D FFT)')

        i=i+1
        if(i>30*20):# for 30 FPS to preview 120 Seconds for the duration time.
            # Save in memory video frame to bmp file.
            cf.VideoFrameSave("Negative.bmp")
            cfCrop.VideoFrameSave("Crop.bmp")
            print("FrameFreq: {}".format(FrameFreq))
            break
    rr.PreviewStop()

#=================================================================================================================
VideoFrameProcessingSimple()



    
