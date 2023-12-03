package com.ssj.sfwebsystem.controller.vo;

// 用于展示图片的VO，一行展示四个图像
public class ImageListVO {
    private String imagePath1;
    private String imagePath2;
    private String imagePath3;
    private String imagePath4;

    public ImageListVO() {
    }

    public ImageListVO(String imagePath1, String imagePath2, String imagePath3, String imagePath4) {
        this.imagePath1 = imagePath1;
        this.imagePath2 = imagePath2;
        this.imagePath3 = imagePath3;
        this.imagePath4 = imagePath4;
    }

    public String getImagePath1() {
        return imagePath1;
    }

    public void setImagePath1(String imagePath1) {
        this.imagePath1 = imagePath1;
    }

    public String getImagePath2() {
        return imagePath2;
    }

    public void setImagePath2(String imagePath2) {
        this.imagePath2 = imagePath2;
    }

    public String getImagePath3() {
        return imagePath3;
    }

    public void setImagePath3(String imagePath3) {
        this.imagePath3 = imagePath3;
    }

    public String getImagePath4() {
        return imagePath4;
    }

    public void setImagePath4(String imagePath4) {
        this.imagePath4 = imagePath4;
    }
}
