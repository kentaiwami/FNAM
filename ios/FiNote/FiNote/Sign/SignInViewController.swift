//
//  SignInViewController.swift
//  FiNote
//
//  Created by 岩見建汰 on 2018/01/21.
//  Copyright © 2018年 Kenta. All rights reserved.
//

import Eureka

class SignInViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        self.tabBarController?.navigationItem.title = "Sign In"
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
}