// Lightweight calculator logic supporting mouse clicks and keyboard typing

class Calculator {
  constructor(prevOperandElement, currentOperandElement) {
    this.prevOperandElement = prevOperandElement;
    this.currentOperandElement = currentOperandElement;
    this.clear();
  }

  clear() {
    this.currentOperand = '0';
    this.previousOperand = '';
    this.operation = undefined;
    this.shouldResetScreen = false;
  }

  delete() {
    if (this.shouldResetScreen) {
      this.clear();
      return;
    }
    if (this.currentOperand.length === 1 || this.currentOperand === '0') {
      this.currentOperand = '0';
    } else {
      this.currentOperand = this.currentOperand.slice(0, -1);
    }
  }

  invertSign() {
    if (this.currentOperand === '0') return;
    if (this.currentOperand.startsWith('-')) {
      this.currentOperand = this.currentOperand.slice(1);
    } else {
      this.currentOperand = '-' + this.currentOperand;
    }
  }

  appendNumber(number) {
    if (this.shouldResetScreen) {
      this.currentOperand = '';
      this.shouldResetScreen = false;
    }
    if (number === '.' && this.currentOperand.includes('.')) return;
    if (this.currentOperand === '0' && number !== '.') {
      this.currentOperand = number.toString();
    } else {
      this.currentOperand = this.currentOperand.toString() + number.toString();
    }
  }

  chooseOperation(operation) {
    if (operation === '%') {
      const current = parseFloat(this.currentOperand);
      if (isNaN(current)) return;
      this.currentOperand = (current / 100).toString();
      this.shouldResetScreen = true;
      return;
    }

    if (this.currentOperand === '') return;
    if (this.previousOperand !== '') {
      this.compute();
    }

    this.operation = operation;
    this.previousOperand = this.currentOperand;
    this.shouldResetScreen = true;
  }

  compute() {
    let computation;
    const prev = parseFloat(this.previousOperand);
    const current = parseFloat(this.currentOperand);

    if (isNaN(prev) || isNaN(current)) return;

    switch (this.operation) {
      case '+':
        computation = prev + current;
        break;
      case '-':
        computation = prev - current;
        break;
      case '×':
      case '*':
        computation = prev * current;
        break;
      case '÷':
      case '/':
        if (current === 0) {
          this.currentOperand = 'Cannot divide by 0';
          this.previousOperand = '';
          this.operation = undefined;
          this.shouldResetScreen = true;
          return;
        }
        computation = prev / current;
        break;
      default:
        return;
    }

    // Round long floating points neatly
    computation = Math.round((computation + Number.EPSILON) * 1e10) / 1e10;

    this.currentOperand = computation.toString();
    this.operation = undefined;
    this.previousOperand = '';
    this.shouldResetScreen = true;
  }

  getDisplayNumber(number) {
    if (number === 'Cannot divide by 0') return number;
    const stringNumber = number.toString();
    const integerDigits = parseFloat(stringNumber.split('.')[0]);
    const decimalDigits = stringNumber.split('.')[1];
    let integerDisplay;

    if (isNaN(integerDigits)) {
      integerDisplay = '';
    } else {
      integerDisplay = integerDigits.toLocaleString('en', { maximumFractionDigits: 0 });
    }

    if (decimalDigits != null) {
      return `${integerDisplay}.${decimalDigits}`;
    } else {
      return integerDisplay || '0';
    }
  }

  updateDisplay() {
    this.currentOperandElement.innerText = this.getDisplayNumber(this.currentOperand);
    if (this.operation != null) {
      this.prevOperandElement.innerText = `${this.getDisplayNumber(this.previousOperand)} ${this.operation}`;
    } else {
      this.prevOperandElement.innerText = '';
    }
  }
}

// Wire up events
document.addEventListener('DOMContentLoaded', () => {
  const prevOperandElement = document.getElementById('previous-operand');
  const currentOperandElement = document.getElementById('current-operand');
  const calc = new Calculator(prevOperandElement, currentOperandElement);

  // Click listeners
  document.querySelectorAll('[data-number]').forEach(button => {
    button.addEventListener('click', () => {
      calc.appendNumber(button.getAttribute('data-number'));
      calc.updateDisplay();
    });
  });

  document.querySelectorAll('[data-operation]').forEach(button => {
    button.addEventListener('click', () => {
      calc.chooseOperation(button.getAttribute('data-operation'));
      calc.updateDisplay();
    });
  });

  document.querySelectorAll('[data-action]').forEach(button => {
    button.addEventListener('click', () => {
      const action = button.getAttribute('data-action');
      if (action === 'clear') calc.clear();
      else if (action === 'delete') calc.delete();
      else if (action === 'invert') calc.invertSign();
      else if (action === 'equals') calc.compute();
      calc.updateDisplay();
    });
  });

  // Keyboard navigation support
  window.addEventListener('keydown', (e) => {
    if ((e.key >= '0' && e.key <= '9') || e.key === '.') {
      calc.appendNumber(e.key);
      calc.updateDisplay();
    } else if (e.key === '+' || e.key === '-') {
      calc.chooseOperation(e.key);
      calc.updateDisplay();
    } else if (e.key === '*') {
      calc.chooseOperation('×');
      calc.updateDisplay();
    } else if (e.key === '/') {
      e.preventDefault();
      calc.chooseOperation('÷');
      calc.updateDisplay();
    } else if (e.key === '%') {
      calc.chooseOperation('%');
      calc.updateDisplay();
    } else if (e.key === 'Enter' || e.key === '=') {
      e.preventDefault();
      calc.compute();
      calc.updateDisplay();
    } else if (e.key === 'Backspace') {
      calc.delete();
      calc.updateDisplay();
    } else if (e.key === 'Escape') {
      calc.clear();
      calc.updateDisplay();
    }
  });

  calc.updateDisplay();
});

