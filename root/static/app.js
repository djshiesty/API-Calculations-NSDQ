async function loadData() {
    const ticker = document.getElementById("ticker").value;
    const res = await fetch("/index?ticker=" + encodeURIComponent(ticker));
    const data = await res.json();
    
    document.getElementById("as-of").textContent = "As of " + data.As_of;
    document.getElementById("price").textContent = "$" + data.Latest_price.toLocaleString();
    document.getElementById("vol").textContent = (data.Volatility_30_days * 100).toFixed(2) + "%";
    document.getElementById("dd").textContent = data.Max_drawdown_pct.toFixed(2) + "%";

    const ivr = data.Implied_and_Realized;
    document.getElementById("spread").textContent = (ivr.spread * 100).toFixed(2) + "%";
    document.getElementById("implied").textContent = (ivr.implied_vol * 100).toFixed(2) + "%";
    document.getElementById("realized").textContent = (ivr.realized_vol * 100).toFixed(2) + "%";
    document.getElementById("interpretation").textContent = ivr.interpretation;
}

document.getElementById("ticker").addEventListener("change", loadData);
loadData();
setInterval(loadData, 60000);