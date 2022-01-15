var xypos = [0,0];
const r = 25;
const margin = 1.5;
const xSquares = 20; // number of columns
const ySquares = 15; // number of rows
const nBombs = 1;//40; // number of bombs in this square
var mask; // binary array, init as all zeros, if zero you cannot see the board tile underneath
var flag;
const leftx = 0; // how much margin to leave on tip
const topy = 50;
var board;
var strBoard;
var startTime;
var endTime;
const colormap = {"1":"#33F","2":"#093","3":"#D33","4":"#00C",
                  "5":"#099","6":"#C00","7":"#0C0","8":"#000",
                  "!!":"#D33"};
var curTime;
var gameState; // "playing" , "won" , "lost"


function startOver() {
  flag = zeros([xSquares,ySquares]);
  mask = zeros([xSquares,ySquares]);
  board = generateBoard();
  strBoard = getStringRepBoard(board);
  startTime = millis();
  gameState = "playing";
}

function setup() {
  createCanvas(r * xSquares + leftx, r * ySquares + topy);
  startOver();
  
  button = createButton('Start Over');
  button.position(0, 0);
  button.mousePressed(startOver);
  
  // tests
  console.log(board[0]);
  console.log(strBoard[0]);
  console.log(mask[0]); // should be all zeros
}

function draw() {
  background("#DDF");
  
  if (gameState == "playing") {
    // draw a timer
    curTime = millis();
    fill("#000");
    textSize(25);
    text( millisToString(curTime - startTime), 100, 30);
  } else if (gameState == "lost") {
    fill("#A00");
    textSize(25);
    text( millisToString(endTime - startTime), 100, 30);
  } else if (gameState == "won") {
    fill("#0A0");
    textSize(25);
    text( millisToString(endTime - startTime), 100, 30);
  }
  drawBoard();
}

function millisToString(t) {
  return parseInt(t / 3600000) + "h " + parseInt((t / 60000) % 60) + "' " + parseInt((t / 1000) % 60) + "''";
}

// helper
function zeros(dimensions) {
  var array = [];
  for (var i = 0; i < dimensions[0]; ++i) {
    array.push(dimensions.length == 1 ? 0 : zeros(dimensions.slice(1)));
  }
  return array;
}

function ones(dimensions) {
  var array = [];
  for (var i = 0; i < dimensions[0]; ++i) {
    array.push(dimensions.length == 1 ? 1 : ones(dimensions.slice(1)));
  }
  return array;
}

// helper function for getting random subarray
function getRandomSubarray(arr, size) {
    var shuffled = arr.slice(0), i = arr.length, temp, index;
    while (i--) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(0, size);
}

// returns a viewable board with numbers -1 through 8
// -1 means bomb
function generateBoard () {
  // generates 2d (m x n) array of strings marked
  // blank if the tile touches zero bombs,
  // k if they are touching k bombs
  // * if the tile is a bomb
  var board = zeros([xSquares,ySquares]);
  let allIdxs = []; // 1d array
  for (let i=0; i< xSquares * ySquares ; i++) {
    allIdxs.push(i);
  }
  const bombIdxs1D = getRandomSubarray(allIdxs , nBombs);
  for (let i = 0; i < bombIdxs1D.length; i++) {
    board[parseInt(bombIdxs1D[i] / ySquares)][bombIdxs1D[i] % ySquares] = -1;
  }
  // fill non bombs with numbers
  for (let i = 0; i < xSquares; i++) {
    for (let j = 0; j < ySquares; j++) {
      if (board[i][j] != -1) {
        for (let xn = Math.max(i - 1,0); xn < Math.min(i+2,xSquares); xn++) {
          for (let yn = Math.max(j-1,0); yn < Math.min(j+2,ySquares); yn++) {
            if ((i!=xn || j!=yn) && board[xn][yn] == -1) {
              board[i][j] = board[i][j] + 1;
            }
          }
        }
      }
    }
  }
  // more code here for filling other numbers
  return board;
}

function getStringRepBoard (board) {
  var stringRepBoard = []
  for (let i=0; i<board.length; i++) {
    let column = [];
    for (let j=0; j<board[i].length; j++) {
      if (board[i][j] == -1) {
        column.push("*");
      } else if (board[i][j] == 0) {
        column.push("")
      } else {
        column.push(board[i][j].toString());
      }
    }
    stringRepBoard.push(column);
  }
  return stringRepBoard;
}

function drawTileBackground (xCoord,yCoord) {
  rect(leftx + xCoord * r + margin , topy + yCoord * r + margin , r - 2*margin , r - 2*margin);
}

function drawTileValue (xCoord,yCoord,tileValue) {
  fill("#EE5555");
  if (tileValue == "*") {
    fill("#000");
    textSize(30);
    text(tileValue, leftx + xCoord * r + margin + 0.2*r , topy + yCoord * r + margin + 1.15*r);
  } else if (tileValue == "") {
    // don't do anything
  }  else {
    // there is a number to be displayed
    fill(colormap[tileValue]);
    textSize(15);
    text(tileValue, leftx + xCoord * r + margin + 0.25*r , topy + yCoord * r + margin + 0.65*r);
  }
  
}

function drawBoard () {
  // draw the tiles in grey
  let c; // hex color variable
  let tileValue; // the string of that tile value
  for (let xc = 0; xc < xSquares ; xc ++) {
    for (let yc = 0; yc < xSquares ; yc ++) {
      if (mask[xc][yc] == 0 && flag[xc][yc] == 1) {
        c = "#CCF"; // make it lighter and a bit blue if it's flagged
      } else if (mask[xc][yc] == 0 && flag[xc][yc] == 0) {
        c = "#888"; // darker square if it's still not visible to player
      } else {
        c = "#CCC"; // light color if it's visible
      }
      fill(c);
      drawTileBackground(xc,yc);
      if (mask[xc][yc] == 1) {
        // console.log(strBoard[xc][yc]);
        drawTileValue(xc , yc , strBoard[xc][yc]);
      } else if (flag[xc][yc] == 1) {
        drawTileValue(xc , yc , "!!");
      }
    }
  }
  // now draw the cursor's background tile
  if (mask[xypos[0]][xypos[1]] == 0 && flag[xypos[0]][xypos[1]] == 0) {
    c = "#BBB";
  } else if (mask[xypos[0]][xypos[1]] == 0 && flag[xypos[0]][xypos[1]] == 1) {
    c = "#DDF";
  } else {
    c = "FFF";
  }
  fill(c);
  strokeWeight(1.3);
  stroke("#006");
  drawTileBackground(xypos[0],xypos[1]);
  strokeWeight(0);
  if (mask[xypos[0]][xypos[1]] == 1) {
    drawTileValue(xypos[0] , xypos[1] , strBoard[xypos[0]][xypos[1]]);
  } else if (flag[xypos[0]][xypos[1]] == 1) {
    drawTileValue(xypos[0], xypos[1], "!!");
  }
  // for index in all indices
  // if the mask at this index is zero 
    // and there's no flag: draw a grey square
    // if there's a flag: draw a flag
  // if not draw a lighter grey square with the board underneath number underneath it
  // draw a lighter square for the cursor
}

// call this function when you reveal a tile
function unmaskTile (xc,yc) {
  if (board[xc][yc] == -1) {
    // if it's a bomb, unmask everything
    gameState = "lost";
    endTime = millis();
    mask = ones([xSquares,ySquares]);
  } else if (board[xc][yc] == 0) {
    // not touching any bombs, unmask it
    mask[xc][yc] = 1;
    // unmask all of it's neighbours too
    for (let i = Math.max(xc - 1 , 0); i < Math.min(xc + 2 , xSquares); i++) {
      for (let j = Math.max(yc - 1 , 0); j < Math.min(yc + 2 , ySquares); j++) {
        if ((i != xc || j!= yc) && mask[i][j] == 0) {
            // unmask the i,j th tile too
          mask[xc][yc] = 1;
          unmaskTile(i,j);
        }
      }
    }
  } else {
    mask[xc][yc] = 1;
  }
}

// helper for summing an array
function sumArray(accumulator, a) {
  return accumulator + a;
}

// handle key presses

function keyPressed() {
  if (keyCode == UP_ARROW && xypos[1] > 0) {
    xypos[1] --;
  } else if (keyCode == DOWN_ARROW && xypos[1] < (ySquares - 1)) {
    xypos[1] ++;
  } else if (keyCode == RIGHT_ARROW && xypos[0] < (xSquares - 1)) {
    xypos[0] ++;
  } else if (keyCode == LEFT_ARROW && xypos[0] > 0) {
    xypos[0] --;
  } else if (keyCode == ENTER && mask[xypos[0]][xypos[1]] == 0 && flag[xypos[0]][xypos[1]] == 0) {
    unmaskTile(xypos[0],xypos[1]);
  } else if (keyCode == 70 && mask[xypos[0]][xypos[1]] == 0) { // 70 is the keycode for 'f'
    // toggle the flag
    flag[xypos[0]][xypos[1]] += 1;
    flag[xypos[0]][xypos[1]] %= 2;
  } else {
    console.log(keyCode.toString());
  }
  // check to see if the player won
  if (xSquares * ySquares - nBombs == mask.flat().reduce(sumArray,0) && gameState == "playing") {
    gameState = "won";
    endTime = millis();
  }
}


/* 

Future work: link with backend, put scorebord underneath so that things work smoothly

*/
