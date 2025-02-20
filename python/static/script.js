const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");

canvas.width = 300;
canvas.height = 300;

const drawCircle = (event) =>{
    const x = event.pageX;
    const y = event.pageY;

    const radius = 20;

    context.beginPath();
    context.arc(x, y, radius, 0, 2 * Math.PI, false);

    context.fillStyle = "red";
    context.fill();
}

drawCircle()

