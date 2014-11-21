//
//  ViewController.swift
//  ScrabbleAi
//
//  Created by Thomas Chow on 11/20/14.
//  Copyright (c) 2014 Thomas Chow. All rights reserved.
//

import UIKit
import Photos

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate{
    var albumFound: Bool = false
    var assetCollection: PHAssetCollection!
    var photoAsset: PHFetchResult!
    var boardImage  : UIImage!
    var picker : UIImagePickerController = UIImagePickerController()
    

    
    @IBOutlet var boardImageView: UIImageView!
    let context = CIContext(options:nil)
    
    
    @IBAction func uploadBoardPhoto(sender: AnyObject) {
        picker.sourceType = UIImagePickerControllerSourceType.PhotoLibrary
        picker.delegate = self
        picker.allowsEditing = false
        self.presentViewController(picker, animated: true, completion: nil)
        
    }
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    func finishAndUpdate() {
        let selectedImage: UIImage = self.boardImageView.image!
        NSLog("HERE")
        //Call CV
        
        
    }
    
    func imagePickerController(picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [NSObject : AnyObject]) {
        let selectedImage: UIImage = info[UIImagePickerControllerOriginalImage] as UIImage
        self.boardImageView.image = selectedImage
        picker.dismissViewControllerAnimated(true, completion: nil)
        finishAndUpdate()
        
    }
    
    func imagePickerControllerDidCancel(picker: UIImagePickerController!) {
        picker.dismissViewControllerAnimated(true, completion: nil)
    }


}

