package com.ssj.sfwebsystem.util;

import com.drew.imaging.ImageMetadataReader;
import com.drew.imaging.ImageProcessingException;
import com.drew.metadata.Metadata;
import com.drew.metadata.exif.ExifDirectoryBase;
import com.drew.metadata.exif.ExifSubIFDDirectory;
import com.drew.metadata.file.FileSystemDirectory;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

// 给我一个图片的文件，我给你返回图片的拍摄时间
// 如果能够获取exfi信息，使用exfi信息中的创建时间
// 否则，使用文件的最后一次修改时间；
// 否则，使用当前时间；
// 如果出现metadata-extractor无法解析的文件格式，则不作处理。
public class MetaDataExtractor {
    public static String getShootTime(File file){
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy:MM:dd HH:mm:ss");
        try {
            Metadata metadata = ImageMetadataReader.readMetadata(file);
            String dateNow = dtf.format(LocalDateTime.now());
            if(metadata==null){
                return dateNow;
            }else{
                // 如果有exif日期数据
                ExifDirectoryBase exifDir = metadata.getFirstDirectoryOfType(ExifSubIFDDirectory.class);
                if(exifDir!=null){
                    dateNow = exifDir.getString(ExifDirectoryBase.TAG_DATETIME_ORIGINAL);
                    if(dateNow!=null){
                        return dateNow;
                    }
                }
                FileSystemDirectory fileDir = metadata.getFirstDirectoryOfType(FileSystemDirectory.class);
                if(fileDir!=null){
                    Object o = fileDir.getObject(FileSystemDirectory.TAG_FILE_MODIFIED_DATE);
                    if(o!=null){
                        SimpleDateFormat sdf = new SimpleDateFormat("yyyy:MM:dd HH:mm:ss");
                        return sdf.format(o);
                    }
                }
            }
        } catch (ImageProcessingException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return dtf.format(LocalDateTime.now());
    }
}
