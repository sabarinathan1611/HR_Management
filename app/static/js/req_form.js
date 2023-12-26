var socket = io();

var leave_submitBtn = document.querySelector(".leavesubmit");
                    leave_submitBtn.addEventListener('click',function(){
                        console.log("clicked")
                        const leaveDet ={}
                        var Reason = document.getElementById("leave_reason");
                        var FromDate = document.getElementById("from_date");
                        var ToDate = document.getElementById("to_date");
                        leaveDet.reason = Reason.value;
                        leaveDet.from_date = FromDate.value;
                        leaveDet.to_date = ToDate.value;
                        console.log('Form Data:', leaveDet);
                        socket.emit('leave',leaveDet);
                        //document.getElementById("leave_form").reset();
                    });

var late_submitBtn = document.querySelector(".latesubmit");
                    late_submitBtn.addEventListener('click',function(){
                        console.log("clicked")
                        const lateDet ={}
                        var Reason = document.getElementById("late_reason");
                        var FromTime = document.getElementById("from_time");
                        var ToTime = document.getElementById("to_time");
                        lateDet.reason = Reason.value;
                        lateDet.from_time = FromTime.value;
                        lateDet.to_time = ToTime.value;
                        console.log('Form Data:', lateDet);
                        socket.emit('late',lateDet);
                        document.getElementById("late_form").reset();
                    });