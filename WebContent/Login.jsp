<%@ page language="java" contentType="text/html; charset=EUC-KR"
    pageEncoding="EUC-KR"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-KR">
<title>Welcome PNU IPS</title>
</head>
<body>
	<h1> PNU IPS �α��� </h1> 
	<br />
	<form action="LoginConfirm.jsp" method="post">
	<table border="0">
       <tr>
           <th> Email </th> <td> <input name="login_email" type="text"> </td>
       </tr>
       <tr>
           <th> PW </th> <td> <input name="login_pw" type="password">  </td>
       </tr>
   	</table>
   	<br/>		
   	<button> �α��� </button>  <span> <input type="button" value="ȸ������" onClick="location.href='Sign.jsp'"> </span>
   	</form>
   	<br/>
   	<input type="button" value="CSV IMPORT" onClick="location.href='CsvImport.jsp'"> <input type="button" value="ADMIN PAGE" onClick="location.href='AdminPage.jsp'">
</body>
</html>