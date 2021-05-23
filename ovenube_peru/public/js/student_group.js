cur_frm.add_fetch("tdx_c_aula", "room_name", "tdx_c_aulan");

function set_instructor(frm) {
    var tinstructor="";
    $.each(frm.doc.instructors, function(i, row){
        tinstructor += row.instructor;
    })
    frm.set_value('tdx_c_intructor', tinstructor);
    frm.refresh();
}

function set_nombre(frm){
    var tnombre = frm.doc.course + "-" + frm.doc.tdx_c_aulan + "-" + frm.doc.tdx_c_turno + "-" + frm.doc.tdx_c_intructor + "-" + frm.doc.tdx_c_año + "-" + frm.doc.tdx_c_mes + "-" + frm.doc.company;
    
    frm.set_value('student_group_name', tnombre);
    frm.refresh();
}

frappe.ui.form.on('Student Group', {
    validate: function(frm) {
        set_nombre(frm);
    },

    instructor: function(frm) {
        set_instructor(frm);
    }
})    