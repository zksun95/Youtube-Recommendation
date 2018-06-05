

var app = angular.module('plunker', ['nvd3']);

var fileName;
        
        function recordToFilename() {
        var input = document.getElementById('filename'),
            fileName = input.value;
        if (fileName) {
            alert('Recording: ' + fileName);
            // app.value("content", "test");
        // Recorder.record('audio', fileName);
        } else {
            alert('Please enter a filename!');
            input.focus();
            }
        }

// function loop_fresh(){   
//     alert("hello");
// }   
// //重复执行某个方法  
// var t1 = window.setInterval(hello,1000);
// var t2 = window.setInterval("hello()",3000);
// //去掉定时器的方法
// window.clearInterval(t1);




app.controller('MainCtrl', function($scope) {

    $scope.options = {
            chart: {
                type: 'scatterChart',
                height: 450,
                color: d3.scale.category10().range(),
                scatter: {
                    onlyCircles: false
                },
                showDistX: true,
                showDistY: true,
                tooltipContent: function(key) {
                    return '<h3>' + key + '</h3>';
                },
                duration: 350,
                xAxis: {
                    axisLabel: 'X Axis',
                    tickFormat: function(d){
                        return d3.format('.02f')(d);
                    }
                },
                yAxis: {
                    axisLabel: 'Y Axis',
                    tickFormat: function(d){
                        return d3.format('.02f')(d);
                    },
                    axisLabelDistance: -5
                },
                zoom: {
                    //NOTE: All attributes below are optional
                    enabled: false,
                    scaleExtent: [1, 10],
                    useFixedDomain: false,
                    useNiceScale: false,
                    horizontalOff: false,
                    verticalOff: false,
                    unzoomEventType: 'dblclick.zoom'
                }
            }
        };


        $scope.run = true;
        $scope.data = [{ values: []}];

        

        //spark
        socket= new WebSocket('ws://127.0.0.1:2033');
        socket.onopen= function() {
            //socket.send('hello1');
            console.log("connect1");
        };
        socket.onmessage= function(s) {
            console.log("receive some");
            console.log(s);
            console.log(s.data);
            console.log(typeof s.data);
        };
        //kafka
        socket1= new WebSocket('ws://127.0.0.1:2055');
        socket1.onopen= function() {
            //socket1.send('trump');
            console.log("connect2");
        };
        socket1.onmessage= function(s) {
            console.log("receive nothing");
            console.log(s);
            console.log(s.data);
            console.log(typeof s.data);
        };


        socket2= new WebSocket('ws://127.0.0.1:5678');
        socket2.onopen= function() {
            //socket2.send('start');
            console.log("connect3");
            //socket2.send('helllllllooooooooooo');
            //var t1 = window.setInterval("socket2.send('helllllllooooooooooo');console.log('hellllllloooooo');",10000);
        };
        var polarity;
        var typeof_polarity;
        var float_like;
        var float_dislkie;
        var shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'],
            random = d3.random.normal();

        $("#query").click(function(){
            console.log($("#message").val());
            if($("#message").val()!=""){
                console.log($("#message").val());
                socket.send('hello1');
                console.log('socket');
                socket1.send($("#message").val());
                console.log('socket1');
                socket2.send('start');
                console.log('start');
                socket2.send('helllllllooooooooooo');
                console.log('helllllllooooooooooo');
                var t1 = window.setInterval("socket2.send('helllllllooooooooooo');console.log('hellllllloooooo');",10000);
            }
        })
        
        function getRandomInt(max) {
             return Math.floor(Math.random() * Math.floor(max));
        }
        socket2.onmessage= function(s) {
            console.log("receive some");
            console.log(s);
            console.log(s.data);
            var data2 = JSON.parse(s.data);
            polarity = data2['polarity'];

            float_like = parseFloat(data2['like']);
            float_dislike = parseFloat(data2['dislike'])+1;
            title = data2['title'];
            img_url = data2['thumbnails'];
            url = data2['url'];
            like_dislike = float_like/float_dislike;
            console.log("here");
            console.log("like: " + like_dislike);
            $("#view").append("title: " +title + ": " );
            $("#view").append("  score: " + polarity);
            $("#view").append("<a href=\"" + url+ "\">go to movie</a></br>");
            $("#view").append("<a href=\"" + img_url + "\" title='Click to see full image' target='_blank'>",
                 "<img src=\"" + img_url+ "\" alt='Item 1' />",
             "</a></br>");



            console.log(typeof like_dislike);

            

                    $scope.data[0].values.push({
                        x: like_dislike
                        , y: polarity
                        , size: Math.random()+1
                        , shape: shapes[getRandomInt(6)]
                    });
                // if ($scope.data[0].values.length > 20) $scope.data[0].values.shift();       x++;
        $scope.$apply(); // update both chart
            
        };

        // setInterval(function(){
        // var data = [],
        //     shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'],
        //     random = d3.random.normal();

        // $scope.data[0].values.push({
        //                 x: 0
        //                 , y: polarity
        //                 , size: Math.random()
        //                 , shape: shapes[2 % 6]
        //             });
        //         // if ($scope.data[0].values.length > 20) $scope.data[0].values.shift();       x++;
        // $scope.$apply(); // update both chart

        

        // if (!$scope.run) return;
        //     while(false){
        //         $scope.data[0].values.push({
        //                 x: 0
        //                 , y: polarity
        //                 , size: Math.random()
        //                 , shape: shapes[2 % 6]
        //             });
        //         // if ($scope.data[0].values.length > 20) $scope.data[0].values.shift();       x++;
        
        //         $scope.$apply(); // update both chart
        //     }
            
        // }, 2000);   
});
