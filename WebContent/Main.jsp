<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR"%>
    
<%
String sessionName = (String)session.getAttribute("user_lastname") + " " + (String)session.getAttribute("user_firstname") ;
String sessionGrade = (String)session.getAttribute("user_grade") ;
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
<title>PNU IPS</title>
</head>
<body>
<div style="float:right"> [<%=sessionGrade%>] <%=sessionName%> ��  ȯ���մϴ�~ <input type="button" value="�α׾ƿ�" onClick="location.href='Logout.jsp'"> </div>
<input type="button" value="īƮ" onClick="location.href='Cart.jsp'">
<h1> PNU IPS �˻� </h1> 

<br />
<br />
<form action="ItemSearch.jsp" method="post">
	<table border="0">
       <tr>
           <th> ��ǰã�� </th> <td> <input name="search_itemName" type="text"> <button> �˻� </button>  </td>
       </tr>
   	</table>
</form>
</body>
</html>