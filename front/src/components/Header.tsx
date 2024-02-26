import { BrowserRouter, Link, Route, Routes, useLocation} from "react-router-dom";
import React, { useState, useEffect } from "react";

const Header = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const isRoot = currentPath === "/";

  return (
    <div className="fixed w-screen z-50">
      <div className="h-16 bg-black bg-opacity-100 justify-center items-center flex">
         <div className="text-sm md:text-4xl font-bold">
          <img src="image/logo_black_text.png" className="h-12"/>
        </div>
      </div>
    </div>
  );
};

export default Header;