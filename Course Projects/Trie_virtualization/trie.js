class TrieNode {
    constructor() {
        this.children = new Array(26).fill(null);
        this.index;
        this.isEndOfWord = false;
    }
}
 
class Trie {
    constructor() {
        this.indexCounter = 0;
        this.root = new TrieNode();
    }

    insert(word) {
        let current = this.root;
        for (let i = 0; i < word.length; i++) {
            let index = word.charCodeAt(i) - 'a'.charCodeAt(0);
            if (!current.children[index]) {
                current.children[index] = new TrieNode();
            }
            current = current.children[index];
        }
        current.isEndOfWord = true;
    }

    searchWithHighlight(word) {
        let current = this.root;
        let svg = document.getElementById("trie-visualization");
        let delay = 500; // Delay between highlighting each character
        return this.highlightNode(current, svg, word, 0, delay);
    }

    async highlightNode(node, svg, word, index, delay) {
        if (!node) return false;
        console.log(node.index);
        // Highlight the current node
        let circle = svg.querySelector(`circle[data-index="${node.index}"]`);

        let sumPromise = new Promise(function (resolve, reject) {
            circle.setAttribute("fill", "red");
            setTimeout(() => {
                resolve();
            }, delay);
        });

        await sumPromise;
        circle.setAttribute("fill", node.isEndOfWord ? "#ffcc00" : "#f0f0f0");

        if (index === word.length) {
            console.log(node.isEndOfWord);
            return node.isEndOfWord;
        }

        let charIndex = word.charCodeAt(index) - 'a'.charCodeAt(0);
        return this.highlightNode(node.children[charIndex], svg, word, index + 1, delay);
    }

    search(word) {
        let current = this.root;
        for (let i = 0; i < word.length; i++) {
            let index = word.charCodeAt(i) - 'a'.charCodeAt(0);
            if (!current.children[index]) {
                return false;
            }
            current = current.children[index];
        }
        return current && current.isEndOfWord;
    }

    remove(word) {
        if (!this.search(word)) {
            return false;
        }
        let current = this.root;
        for (let i = 0; i < word.length; i++) {
            let index = word.charCodeAt(i) - 'a'.charCodeAt(0);
            current = current.children[index];
        }
        current.isEndOfWord = false;
        return true;
    }

    getHeight(node) {
        if (!node) return 0;
        let maxChildHeight = 0;
        for (let child of node.children) {
            maxChildHeight = Math.max(maxChildHeight, this.getHeight(child));
        }
        return 1 + maxChildHeight;
    }

    visualize() {
        this.indexCounter = 0;
        let svg = document.getElementById("trie-visualization");
        svg.innerHTML = ""; 
        let height = this.getHeight(this.root) * 70; 
        let width = this.getHeight(this.root) * 80; 
        svg.setAttribute("width", width);
        svg.setAttribute("height", height);
        this.drawNode(this.root, svg, width / 2, 20, width / 2, "");
    }

    
    drawNode(node, svg, x, y, width, prefix) {
        // Draw node
        let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", x);
        circle.setAttribute("cy", y);
        circle.setAttribute("r", 20);
        circle.setAttribute("fill", node.isEndOfWord ? "#ffcc00" : "#f0f0f0"); // Change color if it's the end of a word
        circle.setAttribute("stroke", "#000");
        let ind = this.indexCounter++;
        node.index = ind; // Assign unique index
        circle.setAttribute("data-index", ind); // Unique index for identification
        svg.appendChild(circle);
    
        // Draw label
        let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", x);
        text.setAttribute("y", y + 5);
        text.setAttribute("text-anchor", "middle");
        text.textContent = prefix;
        svg.appendChild(text);
    
        // Draw edges to children
        let childCount = node.children.filter(child => child !== null).length;
        let childWidth = childCount * 40; // Adjusted child width
        let childX = x - childWidth / 2;
        let index = 0;
        
        for (let i = 0; i < 26; ++i) {
            if (node.children[i]) {
        
                let childCenterX = childX + (index + 0.5) * (childWidth/childCount  );
                let childCenterY = y + 60;
                this.drawEdge(svg, x, y + 20, childCenterX, childCenterY);
                this.drawNode(node.children[i], svg, childCenterX, childCenterY, childWidth / childCount, String.fromCharCode('a'.charCodeAt(0) + i));
                index++;
            }
        }
    }

    countDescendants(node) {
        if (!node) return 0;
        let count = 0;
        for (let child of node.children) {
            count += this.countDescendants(child);
        }
        return count + 1;
    }


    drawEdge(svg, x1, y1, x2, y2) {
        let line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", x1);
        line.setAttribute("y1", y1);
        line.setAttribute("x2", x2);
        line.setAttribute("y2", y2);
        line.setAttribute("stroke", "#000");
        svg.appendChild(line);
    }
}

const trie = new Trie();

function insertWord() {
    let word = document.getElementById("word-input").value.trim();
    if (word !== "") {
        trie.insert(word);
        trie.visualize();
        updateStatus("Word inserted: " + word);
    } else {
        updateStatus("Please enter a word.");
    }
    document.getElementById("word-input").value = "";
}

async function searchWord() {
    let word = document.getElementById("word-input").value.trim();
    if (word !== "") {
        let found = await trie.searchWithHighlight(word);
        console.log(found);
        if (found) {
            updateStatus("Word found: " + word);
        } else {
            updateStatus("Word not found: " + word);
        }
    } else {
        updateStatus("Please enter a word.");
    }
    document.getElementById("word-input").value = "";
}

function deleteWord() {
    let word = document.getElementById("word-input").value.trim();
    if (word !== "") {
        if (trie.remove(word)) {
            trie.visualize();
            updateStatus("Word deleted: " + word);
        } else {
            updateStatus("Word not found: " + word);
        }
    } else {
        updateStatus("Please enter a word.");
    }
    document.getElementById("word-input").value = "";
}

function updateStatus(message) {
    document.getElementById("status").textContent = message;
}


    // drawNode(node, svg, x, y, width, prefix) {
    //     // Draw node
    //     let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    //     circle.setAttribute("cx", x);
    //     circle.setAttribute("cy", y);
    //     circle.setAttribute("r", 20);
    //     circle.setAttribute("fill", node.isEndOfWord ? "#ffcc00" : "#f0f0f0"); // Change color if it's the end of a word
    //     circle.setAttribute("stroke", "#000");
    //     let index = this.indexCounter++; // Assign unique index
    //     circle.setAttribute("data-index", index); // Unique index for identification
    //     svg.appendChild(circle);

    //     // Draw label
    //     let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    //     text.setAttribute("x", x);
    //     text.setAttribute("y", y + 5);
    //     text.setAttribute("text-anchor", "middle");
    //     text.textContent = prefix;
    //     svg.appendChild(text);

    //     // Draw edges to children
    //     // let childCounts = node.children.map(child => child ? this.countDescendants(child) : 0);
    //     // let totalDescendants = childCounts.reduce((acc, val) => acc + val, 0);
    //     // let childWidths = childCounts.map(count => count * 40 / totalDescendants); // Adjusted child width based on descendants
    //     // let childX = x - (width / 2); // Initial x position for the first child
    //     // let childIndex = 0;
    //     let childCount = node.children.filter(child => child !== null).length;
    //     let childWidth = childCount * 40; // Adjusted child width
    //     let childX = x - childWidth / 2;
    //     for (let i = 0; i < 26; ++i) {
    //         if (node.children[i]) {
    //             let childCenterX = childX + (index + 0.5) * (childWidth / childCount);
    //             let childCenterY = y + 60;
    //             this.drawEdge(svg, x, y + 20, childCenterX, childCenterY);
    //             this.drawNode(node.children[i], svg, childCenterX, childCenterY, childWidth/childCount, String.fromCharCode('a'.charCodeAt(0) + i));
    //             // childX += childWidths[childIndex];
    //             childIndex++;
    //         }
    //     }
    // }


    // getNodeIndex(startIndex, depth) {
    //     return startIndex * Math.pow(26, depth);
    // }

    
    // drawNode(node, svg, x, y, width, prefix) {
    //     // Draw node
    //     let circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    //     circle.setAttribute("cx", x);
    //     circle.setAttribute("cy", y);
    //     circle.setAttribute("r", 20);
    //     circle.setAttribute("fill", node.isEndOfWord ? "#ffcc00" : "#f0f0f0"); // Change color if it's the end of a word
    //     circle.setAttribute("stroke", "#000");
    //     svg.appendChild(circle);

    //     // Draw label
    //     let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    //     text.setAttribute("x", x);
    //     text.setAttribute("y", y + 5);
    //     text.setAttribute("text-anchor", "middle");
    //     text.textContent = prefix;
    //     svg.appendChild(text);

    //     // Draw edges to children
    //     let childCount = node.children.filter(child => child !== null).length;
    //     let childWidth = childCount * 40; // Adjusted child width
    //     let childX = x - childWidth / 2;
    //     let index = 0;
    //     for (let i = 0; i < 26; ++i) {
    //         if (node.children[i]) {
    //             let childCenterX = childX + (index + 0.5) * (childWidth / childCount);
    //             let childCenterY = y + 60;
    //             this.drawEdge(svg, x, y + 20, childCenterX, childCenterY);
    //             this.drawNode(node.children[i], svg, childCenterX, childCenterY, childWidth / childCount, String.fromCharCode('a'.charCodeAt(0) + i));
    //             index++;
    //         }
    //     }
    // }