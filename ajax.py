from __future__ import unicode_literals
import frappe      
import datetime
from datetime import timedelta
from frappe.utils import getdate
import json
from frappe.model.document import Document
from datetime import date
from frappe.utils.data import getdate
from datetime import datetime,timedelta
from frappe import utils
@frappe.whitelist()
def coupon(rounded,qty,coupon=None):
    coupon_offer = frappe.db.get_all("Coupon Code", filters = {'coupon_code': coupon,}, fields = ['name','coupon_code','pricing_rule','maximum_use'])
    if coupon:   
        for offer_code in coupon_offer:
            if (coupon == offer_code['coupon_code']):
                if int(offer_code['maximum_use']) == 0:
                    frappe.throw("Offer Limited")
                else:
                    max_use_change = frappe.get_doc("Coupon Code", offer_code['name'])
                    max_use_change.maximum_use = int(max_use_change.maximum_use) - 1
                    max_use_change.used = int(max_use_change.used) + 1
                    max_use_change.save()
                    price_rule = frappe.get_doc("Pricing Rule" , offer_code['pricing_rule'])
                    if int(price_rule.min_qty) <= int(qty) and int(price_rule.max_qty) >= int(qty):
                        if int(price_rule.min_amt) <= int(rounded) and int(price_rule.max_amt) >= int(rounded):
                            today = frappe.utils.nowdate()
                            if getdate(price_rule.valid_from) <= getdate(today) <= getdate(price_rule.valid_upto) :
                                if price_rule.rate_or_discount == 'Discount Percentage':
                                    a = {'dis':price_rule.rate_or_discount,'per':price_rule.discount_percentage}
                                    return json.dumps(a)
                                    # return (price_rule.rate_or_discount,price_rule.discount_percentage)
                                    # frappe.throw(price_rule.rate_or_discount)
                                elif price_rule.rate_or_discount == 'Discount Amount':
                                    a = {'dis':price_rule.rate_or_discount,'per':price_rule.discount_amount}
                                    return json.dumps(a)                                   
                                    # return {'dis':price_rule.rate_or_discount,'per':price_rule.discount_amount}
                                    # frappe.throw(price_rule.rate_or_discount)
                                else:
                                        frappe.throw("Price Rule Error")
                            else:
                                frappe.throw("Offer Period Not Matching")    
                            
                        else:
                            frappe.throw("amount not matching")
                    else:
                        frappe.throw("Qty not matching")
            else:
                frappe.throw("enter Valid code")        
    elif coupon == None:
        frappe.throw("enter coupon")

    # coupon_offer = frappe.get_doc("Coupon Code", 'April Offer')
    # price_rule = frappe.get_doc("Pricing Rule", 'Pos Rule')  
    # if coupon == coupon_offer.coupon_code:
    #     if int(qty) > int(price_rule.min_qty) and int(qty) < int(price_rule.max_qty):
    #         if int(rounded) > int(price.min_amt) and int(rounded) < int(price.max_amt):
    #             return int(price_rule.discount_percentage)
    #         else:
    #             frappe.throw("Amount Is Not Matching")
    #     else:
    #         frappe.throw("Quantity Is Not Matching")
    # else:
    #     frappe.throw("Enter Valid Code")
        

# for i in range (0,len(offer_period)):
                    #     today = frappe.utils.nowdate()
                    #     if getdate(today) == getdate(offer_period[i]):
                    #         frappe.throw("Offer Period Not Matching")

# for i in range (0,len(offer_period)):
                            #     today = frappe.utils.nowdate()
                            #     frappe.throw(frappe.as_json(getdate(offer_period))
    
    # delta = getdate(price_rule.valid_upto) - getdate(price_rule.valid_from) 
                    # for i in range(delta.days + 1):
                    #     dates = getdate(price_rule.valid_from) + timedelta(days = i)
                    #     offer_period.append(dates)


#...........................javascript....................................#
    # frappe.ui.form.on('Sales Invoice', {
    # refresh(frm){ 
    #     // var div = document.querySelector("body");
    #     var button = document.createElement("BUTTON");
    #     button.innerHTML = "Add Coupon";
    #     let container = document.querySelector('div.clearfix');
    #     button.style.backgroundColor="blue";
    #     button.style.color="white";
    #     container.appendChild(button);
    #     button.onclick = function() {
    #         let d = new frappe.ui.Dialog({
    #         title: 'Enter details',
    #         fields: [
    #         {
    #             label: 'Coupon Code',
    #             fieldname: 'coupon_code',
    #             fieldtype: 'Data'
    #         }
       
    #         ],
    #         primary_action_label: 'Submit',
    #         primary_action(values) {
    #             frappe.call({
    #                 method: 'frappino.ajax.ajax.coupon',
    #                 args: {
    #                       coupon: d.get_values().coupon_code,
    #                       docname :frm.doc.name,
    #                       rounded :frm.doc.rounded_total,
    #                       qty :frm.doc.total_qty
    #                     //   fieldname:['coupon':'coupon_code']
    #                 //   customer_id: cur_frm.doc.customer_id,
    #                 //   venue: cur_frm.doc.venue,
    #                 //   date: cur_frm.doc.date,
    #                 //   ending_date: cur_frm.doc.ending_date, 
    #                 },
    #                 callback:function(r){
    #                     var l= JSON.parse(r.message);
    #                     var discount_percentage=document.querySelector("input.additional_discount_percentage");
    #                     var discount_amount = document.querySelector("input.discount_amount");
    #                     if (l.dis ==='Discount Amount'){
    #                         var amount = l.per;
    #                         discount_amount.value = amount;
    #                         discount_amount.dispatchEvent(new Event('change'));
                            
    #                     }
    #                     else if(l.dis ==='Discount Percentage'){
    #                         var percentage = parseInt(l.per);
    #                         discount_percentage.value = percentage;
    #                         discount_percentage.dispatchEvent(new Event('change'));
    #                     }
    #                     // var b = JSON.parse(a);
    #                     // for(var i = 0; i < b.length; i++)
    #                     // {
    #                     //     var c = b[i]['message'];
    #                     //     
    #                     // }
    #                     // var obj = Number(a);
    #                     // var b = typeof a
                        
                        
    #                     // frappe.throw(a);
    #                     // x = a.name;
    #                     // var x = a['message'];
                        
    #                     // var s = JSON.stringify(a[0].message);
    #                     // var d = JSON.parse(s);
    #                     // // var s = a[0].message + "";
    #                     // var d = parseInt(s);
    #                     // frappe.throw(d)
                        
                        
    #                     // var d = JSON.parse(a)[0];
    #                     // frappe.throw(d)
    #                     // name.value = a[1];
    #                     // name.textContent=10;
    #                     // name.appendChild(document.createElement('div')).textContent=10;
    #                     // // name.appendChild(document.createTextNode(10));
    #                     // // let namee = document.querySelector('div.form-control additional_discount_percentage text-right');
    #                     // // container = 50;
                        
    #                     // // console.log(container)
    #                     // cur_frm.set_value("additional_discount_percentage",10);
                
    #                 }
    #                 });
    #             d.hide();
    #         }
    #     });

    #     d.show();

    #         };
    #     }

    #     });
    #gsdfgdfggsfgs