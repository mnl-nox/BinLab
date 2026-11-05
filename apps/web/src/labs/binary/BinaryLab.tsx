import { useMemo, useState } from "react";
import { ArrowLeftRight, Binary, BookOpen } from "lucide-react";
import { bitwiseOperation, convertInteger, formatInteger, parseInteger, type NumericBase } from "../../domain/numbers";

const baseOptions: { value: NumericBase; label: string }[] = [
  { value: 2, label: "Binário · 2" },
  { value: 8, label: "Octal · 8" },
  { value: 10, label: "Decimal · 10" },
  { value: 16, label: "Hexadecimal · 16" }
];

function errorMessage(error: unknown): string {
  return error instanceof Error ? error.message : "Falha inesperada ao processar a entrada.";
}

export default function BinaryLab() {
  const [input, setInput] = useState("255");
  const [base, setBase] = useState<NumericBase>(10);
  const [left, setLeft] = useState("1100");
  const [right, setRight] = useState("1010");
  const [operator, setOperator] = useState<"&" | "|" | "^" | "<<">("&");

  const conversion = useMemo(() => {
    try {
      return { value: convertInteger(input, base), error: null };
    } catch (error) {
      return { value: null, error: errorMessage(error) };
    }
  }, [input, base]);

  const bitCalculation = useMemo(() => {
    try {
      const a = parseInteger(left, 2);
      const b = parseInteger(right, operator === "<<" ? 10 : 2);
      return { value: formatInteger(bitwiseOperation(a, operator, b), 2), error: null };
    } catch (error) {
      return { value: null, error: errorMessage(error) };
    }
  }, [left, right, operator]);

  return (
    <div className="lab-content">
      <div className="section-heading">
        <div>
          <span className="eyebrow">LABORATÓRIO 01 / FUNDAMENTOS</span>
          <h2>Binary & Logic Lab</h2>
          <p>Explore representações numéricas e operações bit a bit sem enviar dados para serviços externos.</p>
        </div>
        <span className="live-indicator"><i /> Execução local</span>
      </div>
      <div className="tool-grid">
        <section className="panel converter-panel">
          <div className="panel-heading">
            <div className="panel-icon"><ArrowLeftRight size={18} /></div>
            <div><h3>Conversor de bases</h3><p>Um inteiro, quatro representações</p></div>
          </div>
          <label className="field-label" htmlFor="number-input">Valor de entrada</label>
          <div className="input-row">
            <input id="number-input" value={input} onChange={(event) => setInput(event.target.value)} spellCheck={false} autoComplete="off" aria-describedby="conversion-error" />
            <select aria-label="Base de entrada" value={base} onChange={(event) => setBase(Number(event.target.value) as NumericBase)}>
              {baseOptions.map((option) => <option key={option.value} value={option.value}>Base {option.value}</option>)}
            </select>
          </div>
          {conversion.error && <p id="conversion-error" className="error-text" role="alert">{conversion.error}</p>}
          <div className="result-list">
            {baseOptions.map((option) => (
              <div className="result-row" key={option.value}><span>{option.label}</span><code>{conversion.value?.[option.value] ?? "—"}</code></div>
            ))}
          </div>
          <p className="helper-text">Inteiros via BigInt. A saída usa prefixos 0b, 0o e 0x para identificar as bases.</p>
        </section>
        <section className="panel logic-panel">
          <div className="panel-heading">
            <div className="panel-icon"><Binary size={18} /></div>
            <div><h3>Operações bit a bit</h3><p>Manipulação direta de bits</p></div>
          </div>
          <label className="field-label" htmlFor="operand-a">Operando A · binário</label>
          <input id="operand-a" className="full-input mono" value={left} onChange={(event) => setLeft(event.target.value)} spellCheck={false} />
          <div className="operator-row">
            <label className="field-label" htmlFor="operator">Operação</label>
            <select id="operator" value={operator} onChange={(event) => setOperator(event.target.value as typeof operator)}>
              <option value="&">AND · &</option><option value="|">OR · |</option><option value="^">XOR · ^</option><option value="<<">SHIFT LEFT · &lt;&lt;</option>
            </select>
          </div>
          <label className="field-label" htmlFor="operand-b">{operator === "<<" ? "Deslocamento · decimal" : "Operando B · binário"}</label>
          <input id="operand-b" className="full-input mono" value={right} onChange={(event) => setRight(event.target.value)} spellCheck={false} />
          {bitCalculation.error
            ? <p className="error-text" role="alert">{bitCalculation.error}</p>
            : <div className="logic-result"><span>Resultado</span><code>{bitCalculation.value}</code></div>}
          <p className="helper-text">O deslocamento é limitado a 4096 posições. Os operandos são interpretados como inteiros.</p>
        </section>
      </div>
      <section className="note-panel">
        <BookOpen size={18} />
        <div>
          <strong>Modelo mental</strong>
          <p>Uma operação bit a bit trabalha sobre a representação inteira. AND mantém bits presentes nos dois operandos; OR combina bits; XOR mantém posições diferentes; deslocamento move os bits. Atenção: BigInt usa semântica de inteiro com sinal e extensão de sinal, não um registrador de largura fixa. A simulação de registradores de N bits exigirá máscara explícita.</p>
        </div>
      </section>
    </div>
  );
}
