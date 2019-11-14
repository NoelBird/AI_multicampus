# JavaScript



## 변수

```javascript
// 00_variable.js

/* 
1. let
    - 값을 재할당할 수 있는 변수를 선언하는 키워드
    - 할당은 여러 번 가능하다.
    - 블록 유효 범위(block scope)를 갖는 지역변수 생성
    - (블록 유효 범위는 if, for문 그리고 함수에서 중괄호 내부)
    - 선언과 동시에 원하는 값으로 초기화    
*/
let x = 1
// let x = 2 // already declared 에러 발생

if (x === 1) {
    let x = 5
    console.log(x)
}

console.log(x)

/* 
2. const
    - 값이 변하지 않는 상수를 선언하는 키워드
    - 재할당을 통해 바뀔 수 없고, 재선언 될 수 없음
    - let과 동일하게 블록 유효 범위(block scope)를 가지고 있음
*/
// const MY_FAV
const MY_FAV = 7
console.log('my favorite number is: ' + MY_FAV)

MY_FAV = 20
const MY_FAV = 50

if (MY_FAV === 7) {
    const MY_FAV = 20
    console.log('my favorite number is: ' + MY_FAV)
}
console.log(MY_FAV)

/*
3. var
    - ES6 이전 feature로 문제를 많이 발생시키는 키워드. 절대 사용하지 않는다.
    - var로 선언된 변수의 범위는 현재 실행 문맥인데, 그 문맥은 함수 혹은
      외부 전역으로도 갈 수 있다.
    - Hoisting(선언 끌어올리기)과 같은 현상등의 문제를 발생시키는 요인이다.
*/
function varTest() {
    var x = 1
    if (true) {
        var x = 2
        console.log(x)
    }
    console.log(x)
}
varTest()

function letTest() {
    let x = 1
    if (true) {
        let x = 2
        console.log(x)
    }
    console.log(x)
}
letTest()

/* 
    정리
    1. var - 할당 및 선언 자유, 함수 스코프
    2. let - 할당 자유, 선언은 한번만, 블록 스코프
    3. const - 할당 및 선언 한번만, 블록 스코프
*/

/*
4. 식별자
    - 변수명은 식별자라고 불리며, 특정 규칙을 따른다. 
    - 반드시 문자, 달러($) 또는 밑줄로 시작해야 한다. 
    - 대소문자를 구분하며 클래스명을 제외하고는 대문자로 시작X.
*/

// 숫자, 문자, Boolean
let dog
let variableName

// 배열 - 복수형 이름을 사용
const dogs = []

// 함수
function getPropertyName() {
    ...
}

// Boolean 반환 함수 - 반환 값이 Boolean인 함수는 'is'로 시작
let isAvailable = false

// 클래스, 생성자 (파스칼 케이스 사용)
class User {
    constructor(options) {
        this.name = options.name
    }
}

const good = new User({
    name: 'eric',
})

// 상수 (대문자 스네이크 케이스)
export const API_KEY = 'SOMEKEY'
```



## nodejs 설치 및 테스트

```javascript
// 01_hosting.js

// 된다!
console.log(a)
var a = 10
console.log(a)

// 아래와 같은 과정을 거친다.
var a // 1. 선언이 최상단으로
console.log(a) // 2. 에러가 나지 않고 undefined
a = 10 // 3. 할당은 그 뒤에
console.log(a)

// let은 어떨까?
console.log(b)
let b = 10
console.log(b)
```



## type operator

```javascript
// 02_type_operator.js

// Primitivie 타입
// 1. Numbers
const a = 13
const b = -5
const c = 3.14 // float
const d = 2.998e8
const e = Infinity
const f = -Infinity
const g = NaN // Not a Number. ex) 0/0, "문자"*10 

// 2. String
const sentence1 = 'Ask and go to the blue' // single quote
const sentence2 = "Ask and go to the blue" // double quote
const sentence3 = `Ask and go to the blue` // backtic

// 2-1. 줄바꿈
// const word = "안녕
// 하세요"

const word1 = "안녕 \n하세요" 
console.log(word1)

// 2-2. 리터럴
const word2 = `안녕
하세요`
console.log(word2)

const age = 10
const message = `홍길동은 ${age}`
console.log(message)

const hacking = 'Happy' + 'Hacking' + '!'
console.log(hacking)

// 3. Boolean
true
false

// 4. Empty Value
let first_name
console.log(first_name) // undefined 

let last_name = null
console.log(last_name) // null

typeof null // object
typeof undefined // undefined

// 연산자
// 1. 할당 연산자
let c = 0 

c += 10 
console.log(c) // 10 - C에 10을 더한다. 

c -= 3
console.log(c) // 7 - C에 3을 뺀다. 

c *= 10
console.log(c) // 70 - c에 10을 곱한다.

c++
console.log(c) // 71 - c에 1을 더한다. 

c-- 
console.log(c) // 70 - c에 1을 뺀다. 

// 2. 비교 연산자
// (*참고) 변수 앞에 var, const, let을 붙여주지 않으면
// JS엔진이 자동으로 var를 붙여준다.
3 > 2 // true
3 < 2 // false

'A' < 'B' // true
'Z' < 'a' // true
'가' < '나' // true

// 3. 동등 연산자 (동등 연산자의 사용은 지.양.한다.)
const a = 1
const b = '1'

console.log(a == b) // true
console.log(a != b) // false

// 4. 일치 연산자
console.log(a === b) // false
console.log(a === Number(b)) // true

// 5. 논리 연산자 (and, or, not)
true && false // false
ture && true // true

1 && 0 // 0
0 && 1 // 0
4 && 7 // 7

false || true // true
false || false // false

1 || 0 // 1
0 || 1 // 1
4 || 7 // 4

!true // false

// 6. 삼항 연산자 (Ternary Operator)
true ? 1 : 2 // 1
false ? 1: 2 // 2
'justin' ? 'nice' : 'awesome' // 'nice'

// 조건문과 반복문
// 1. if문
const userName = prompt("Hello! Who are you?")

let message = ''

if (userName === '1q2w3e4r') {
    message = "<h1>This is Secret Admin Page</h1>"
} else if (userName === 'Kang') {
    message = "<h1>Hello, Kang!</h1>"
} else {
    message = `<h1>Hello, ${userName}</h1>`
}

console.log(message)

// 2. switch 문
const userName = prompt("Hello, who are you?")

let message = ''

switch(userName) {
    case '1q2w3e4r': {
        message = "<h1>This is Secret Admin Page</h1>"
        break
    }
    case 'Kang': {
        message = '<h1>Hello, Kang!</h1>'
        break
    }
    default: {
        message = `<h1>Hello, ${userName}</h1>`
    }
}

// 반복문
// 1. while loop
let i = 0

while (i < 6) {
    console.log(i)
    i++
}

// 2. for loop
for (let j = 0; j < 6; j++) {
    console.log(j)
}

const numbers = [0, 1, 2, 3, 4, 5]

for (let number of numbers) {
    console.log(number)
}
```



## 함수

```javascript
// 03_functions.js

// 1. 선언식 (statement, declaration)
// 코드가 실행되기 전에 로드된다.
function add(num1, num2) {
    return num1 + num2
}

add(2, 7) // 9

// 2. 표현식 (exrpession)
// 인터프리터가 해당 코드에 도달했을 때 로드된다.
const sub = function(num1, num2) {
    return num1 - num2 
}

sub(7, 2) // 5

// 3. Arrow Function
const greeting = function(name) {
    return `hello! ${name}`
}

// 3-1. function 키워드 삭제
const greeting = (name) => { return `hello ${name}` }

// 3-2. () 생략 (매개변수가 하나일 경우에만)
const greeting = name => { return `hello ${name}` }

// 3-3. {} & return 생략 (바디에 표현식이 1일 경우)
const greeting = name => `hello ${name}`

// 4. Anonymous Function (익명함수/1회용)
(function (num) { return num ** 3 })(2) // 8 
```



## 자료구조 - 배열

```javascript
// 04_datastructure.js

// 1. 배열
const numbers = [1, 2, 3, 4]

numbers[0] // 1
numbers[-1] // undefined => 정확한 양의 정수만 index 가능
numbers.length

// 원본 파괴
numbers.reverse() // [4, 3, 2, 1]
numbers // [4, 3, 2, 1]

// push - 배열의 길이 return
numbers.push('a') // 5
numbers // [1, 2, 3, 4, 'a']

// pop - 배열의 가장 마지막 요소 제거 후 return
numbers.pop() // 'a'

// unshift - 배열의 가장 앞에 요소 추가
numbers.unshift('a') // 5
numbers // ['a', 1, 2, 3, 4]

// shift - 배열의 가장 첫번째 요소 제거 후 return
numbers.shift() // 'a'
numbers // [1, 2, 3, 4]

numbers.includes(1) // true
numbers.includes(0) // false

numbers.push(4) //
numbers // [1, 2, 3, 4, 4]
numbers.indexOf(4) // 3 => 중복이 존재한다면 처음 찾은 요소의 index
numbers.indexOf('c') // -1 => 찾고자 하는 요소가 없으면 -1

// join - 배열의 요소를 join 
// 함수의 인자를 기준으로 이어서 문자열 return
numbers.join() // 아무것도 넣지 않으면 , 를 기준으로 가져옴. '1,2,3,4,4'
numbers.join('') // 12344
numbers.join('-') // 1-2-3-4-4
```





## 자료구조 - 객체(Object)

객체와 json은 차이가 있습니다.

json은 자바스크립트의 객체 형식을 따르기는 하지만, string 형식인데 반해

자바스크립트의 객체는 string이 아닙니다.



```javascript
// 2. 객체(오브젝트)

const me = {
    name: 'DongWook',
    'phone number': '01022281910',
    appleProducts: {
        ipad: '2018pro',
        iphone: '7+',
        mackbook: '2019pro',
    }
}

me.name // DongWook
me["name"] // DongWook
me["phone number"] // 01022281910

me.appleProducts // { ipad: '2018pro, ....}

// 2-1. Object Literal (ES6+)
// ES5
var books = ['Learning JS', 'Eloquent JS']
var comics = {
    'DC': ['Superman', 'Joker'],
    'Marvel': ['Captain Marvel', 'Avengers'],
}

var magazines = null;

var bookShop = {
    books: books,
    comics: comics,
    magazines: magazines,
}

// ES6
let books = ['Learning JS', 'Eloquent JS']
let comics = {
    'DC': ['Superman', 'Joker'],
    'Marvel': ['Captain Marvel', 'Avengers'],
}

let magazines = null

let bookShop = {
    books,
    comics,
    magazines,
}

// 3. JSON (Javascript Object Notation - JS 객체 표기법)
// Object -> String
const jsonData = JSON.stringify({
    coffee: 'Americano',
    iceCream: 'mint choco',
})

console.log(jsonData) // "{ coffee: 'Americano', iceCream: 'mint choco', }"

// String -> Object
const parsedData = JSON.parse(jsonData)
console.log(parsedData) // { coffee: 'Americano', iceCream: 'mint choco', }
```



## 배열 helper method

```javascript
// 05_array_helper_method.js

// 1. forEach
// array.forEach(callback(element, index, array))
// ES5
var colors = ['red', 'blue', 'green']
for (var i = 0; i < colors.length; i++) {
    console.log(colors[i])
}

// ES6+
const colors = ['red', 'blue', 'green']
colors.forEach(function(color) {
    console.log(color)
})
colors.forEach( color => console.log(color) )

// 2. map
// array.map(callback(element))
// 배열 내의 모든 요소에 대해 각각 주어진 함수를 호출한 결과를
// 모아서 새로운 배열을 return 한다.
const numbers = [1, 2, 3]

const double_numbers = numbers.map(function(num) {
    return num * 2
})
const double_numbers = numbers.map( num => num * 2 )

// 3. filter
// array.filter(callback(element))
// 주어진 함수의 테스트(조건)를 통과하는 모든 요소를 모아
// 새로운 배열을 반환한다.

const products = [
    { name: 'cucumber', type: 'vegetable'},
    { name: 'banana', type: 'fruit'},
    { name: 'apple', type: 'fruit'},
]

const fruit_products = products.filter(function(product) {
    return product.type === 'fruit'
})
fruit_products // [{ name: 'banana', type: 'fruit'}, { name: 'apple', type: 'fruit'}]
```

