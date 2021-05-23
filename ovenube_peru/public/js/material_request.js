cur_frm.cscript.custom_refresh = function(doc) {
    switch(this.frm.doc.company) {
        case "VIVENTIAL":
            cur_frm.doc.naming_series = "MREQ-";
            break;
	case "THE ENGLISH WALKER S.A.C.":
            cur_frm.doc.naming_series = "MREQTEW-";
            break;
	case "BLAIBERG CARRASCO":
            cur_frm.doc.naming_series = "MREQBLG-";
            break;
	case "U-EDUCATION E.I.R.L":
            cur_frm.doc.naming_series = "MREQUED-";
            break;
	case "U-EDUCATION IQUITOS":
            cur_frm.doc.naming_series = "MREQUEDIQT-";
            break;
        default:
            cur_frm.doc.naming_series = "";
            break;
         }
}