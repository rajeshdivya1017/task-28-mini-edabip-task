import {
  BarChart3,
  FileText
} from "lucide-react";

import {
  NavLink
} from "react-router-dom";


export default function Sidebar() {

  return (

    <aside className="sidebar">

      <div className="brand">
        EDABIP
      </div>


      <nav>

        <NavLink
          to="/dashboard"
          className="nav-link"
        >

          <BarChart3 size={18} />

          Dashboard

        </NavLink>


        <NavLink
          to="/reports"
          className="nav-link"
        >

          <FileText size={18} />

          Reports

        </NavLink>

      </nav>

    </aside>
  );
}