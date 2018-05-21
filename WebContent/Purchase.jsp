<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR" import="java.sql.*"%>
<%@ page import="java.lang.String" %>
<%@ page import="connect.DBConnection" %>

<%
String sessionName = (String)session.getAttribute("user_lastname") + " " + (String)session.getAttribute("user_firstname") ;
String sessionEmail = (String)session.getAttribute("user_email") ;
String sessionGrade = (String)session.getAttribute("user_grade") ;

String couponId = request.getParameter("WhatCouponId") ;
int coupon_percent = 0 ;

if (couponId.equals("000000")) {
	coupon_percent = 30 ;
}
else if (couponId.equals("000005")) {
	coupon_percent = 10 ;
}
else {
	coupon_percent = 0 ;
}


int total = 0 ;
int totalPrice = 0 ;
String totalItemString = null ;
int totalPriceDiscount = 0 ;

try {
	//count cart tuple
	Connection conn = DBConnection.getConnection() ;
	Statement st = conn.createStatement() ;
	String sqlCount = "SELECT COUNT(*) FROM cart WHERE user_email='" + sessionEmail + "';" ;
	ResultSet rs = st.executeQuery(sqlCount) ;
	if (rs.next()) {
		total = rs.getInt(1) ;
	}
	rs.close() ;	
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
<title>Purchase !</title>
</head>
<body>
<h1> PNU IPS ���� </h1> 
<div style="float:right"> [<%=sessionGrade%>] <%=sessionName%> ��  ȯ���մϴ�~ <input type="button" value="�α׾ƿ�" onClick="location.href='Logout.jsp'"> </div>
<%
out.print("�� ��ǰ �� : " + total + "��") ;
%>
<br />
<br />
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr height="1" bgcolor="#82B5DF"><td colspan="7" width="752"></td></tr>
<tr height="5"><td width="5"></td></tr>
<tr>
<td width="30">No</td>
<td width="120">��ǰ��</td>
<td width="100">�귣��</td>
<td width="120" style="color:red"><strong>����</strong></td>
<td width="60">���</td>
<td width="60">�Ǹŷ�</td>
<td width="50" style="color:red"><strong>���� ����</strong></td>
</tr>
<tr height="1" bgcolor="#82B5DF"><td colspan="7" width="752"></td></tr>

<%	
	int index = 0 ;
	String sql = "SELECT items.*, cart.item_amount FROM items JOIN cart ON "
			+ "items.item_code=cart.item_code AND items.item_sellerCode=cart.seller_code "
			+ "WHERE user_email='" + sessionEmail + "'";
	rs = st.executeQuery(sql) ;
	
	while (rs.next()) {
		index++ ;
		String item_name = rs.getString("item_name");
		String item_brand = rs.getString("item_brand") ;
		int item_price = rs.getInt("item_price") ;
		int item_numOfStock = rs.getInt("item_stock") ;
		int item_numOfSales = rs.getInt("item_sales") ;
		int item_amount = rs.getInt("item_amount") ;
		
		String item_itemCode = rs.getString("item_code") ;
		String item_sellerCode = rs.getString("item_sellercode") ;
		String item_key = item_itemCode +" "+ item_sellerCode ;
		totalItemString = totalItemString + "," + item_key ;
		totalPrice += (item_price * item_amount) ;		
	%>
	<tr height="25" align="center">
		<td align="left"><%=index %></td>
		<td align="left"><%=item_name %></td>
		<td align="left"><%=item_brand %></td>
		<td align="left" style="color:red"><strong><%=item_price %></strong></td>
		<td align="left"><%=item_numOfStock %></td>
		<td align="left"><%=item_numOfSales %></td>
		<td align="center" style="color:red"><strong><%=item_amount %></strong></td>
	</tr>
	<%
	}
	totalPriceDiscount = totalPrice * (100-coupon_percent) / 100 ;
	%>

<tr height="1" bgcolor="#82B5DF"><td colspan="7" width="752"></td></tr>
</table>
<br />
<br />
<button onClick='history.back();'> �ڷ�  </button>
<br />
<br />
<h2 align="right" > ��ǰ �ݾ� : <%=totalPrice%> �� </h2>
<h2 align="right" > ���� �ݾ� : <%=totalPrice - totalPriceDiscount%>(<%=coupon_percent%>%) </h2>
<h2 align="right" style="color:blue"> ����  �ݾ� : <%=totalPriceDiscount%> �� </h2>
<br />
<form name="form" action="PurchaseConfirm.jsp" method="post" onsubmit="return purChase()">
<P align="right"> <button style="font-size:20px"> PURCHASE!!! </button></P>
<input type="hidden" name="totalItemString" value="<%=totalItemString%>"/>
<input type="hidden" name="totalIndex" value="<%=index%>"/>
<input type="hidden" name="couponId" value="<%=couponId%>"/>
<input type="hidden" name="totalPriceDiscount" value="<%=totalPriceDiscount%>"/>
</form>

<%
} catch (Exception e) {
	out.println("DB ���� ����") ;
}
%>
</body>


<script>
function purChase() {
	var purchaseAmount = <%=totalPriceDiscount%> ;
	alert("�ݾ� " + purchaseAmount + "�� ���� �մϴ�." ) ;
	return true ;
	
}

</script>
</html>