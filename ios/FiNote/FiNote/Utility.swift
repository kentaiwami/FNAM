//
//  Utility.swift
//  FiNote
//
//  Created by 岩見建汰 on 2018/01/21.
//  Copyright © 2018年 Kenta. All rights reserved.
//

import UIKit
import Eureka
import PopupDialog

class Utility {
    func showRowError(row: BaseRow) {
        let rowIndex = row.indexPath!.row
        while row.section!.count > rowIndex + 1 && row.section?[rowIndex  + 1] is LabelRow {
            row.section?.remove(at: rowIndex + 1)
        }
        
        if !row.isValid {
            for (index, err) in row.validationErrors.map({ $0.msg }).enumerated() {
                let labelRow = LabelRow() {
                    $0.title = err
                    $0.cell.height = { 30 }
                    $0.cell.contentView.backgroundColor = UIColor.red
                    $0.cell.textLabel?.font = UIFont.boldSystemFont(ofSize: 13)
                    $0.cell.textLabel?.textAlignment = .right
                    }.cellUpdate({ (cell, row) in
                        cell.textLabel?.textColor = .white
                    })
                row.section?.insert(labelRow, at: row.indexPath!.row + index + 1)
            }
        }
    }

    func getAppDelegate() -> AppDelegate {
        return UIApplication.shared.delegate as! AppDelegate
    }
    
    
    func getBirthYears() -> [String] {
        let date = Date()
        let calendar = Calendar.current
        let year = calendar.component(.year, from: date)
        
        var array = ["誕生年を登録しない"]
        for i in (year-59...year) {
            array.append(String(i))
        }
        
        return array
    }
    
    func isCheckFormValue(form: Form) -> Bool {
        var err_count = 0
        for row in form.allRows {
            err_count += row.validate().count
        }
        
        if err_count == 0 {
            return true
        }
        
        return false
    }
    
    func isHTTPStatus(statusCode: Int?) -> Bool {
        // 200系以外ならエラー
        let code = String(statusCode!)
        var results:[String] = []
        
        if code.pregMatche(pattern: "2..", matches: &results) {
            return true
        }else {
            return false
        }
    }
    
    func showStandardAlert(title: String, msg: String, vc: UIViewController) {
        let button = DefaultButton(title: "OK", dismissOnTap: true) {}
        let popup = PopupDialog(title: title, message: msg)
        popup.transitionStyle = .zoomIn
        popup.addButtons([button])
        vc.present(popup, animated: true, completion: nil)
    }
    
    func uiColorToUIImage(hex: String, alpha: CGFloat) -> UIImage? {
        let rect = CGRect(x: 0, y: 0, width: 1, height: 1)
        UIGraphicsBeginImageContext(rect.size)
        
        let context = UIGraphicsGetCurrentContext()
        context!.setFillColor(UIColor.hex(hex, alpha: alpha).cgColor)
        context!.fill(rect)
        
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        
        return image
    }
    
    func addAttributedTextLineHeight(height: Int, text: NSMutableAttributedString) -> NSMutableAttributedString {
        let lineHeight = CGFloat(height)
        let paragraphStyle = NSMutableParagraphStyle()
        paragraphStyle.minimumLineHeight = lineHeight
        paragraphStyle.maximumLineHeight = lineHeight
        paragraphStyle.lineBreakMode = .byTruncatingTail
        text.addAttribute(NSAttributedString.Key.paragraphStyle, value: paragraphStyle, range: NSMakeRange(0, text.length))
        
        return text
    }
}

class Indicator {
    let indicator = UIActivityIndicatorView()
    
    func showIndicator(view: UIView) {
        indicator.style = .whiteLarge
        indicator.center = view.center
        indicator.color = UIColor.gray
        indicator.hidesWhenStopped = true
        view.addSubview(indicator)
        view.bringSubviewToFront(indicator)
        indicator.startAnimating()
    }
    
    func stopIndicator() {
        self.indicator.stopAnimating()
    }
}
